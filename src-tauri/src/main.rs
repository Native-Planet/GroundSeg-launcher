#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

extern crate sys_info;

use std::fs::File;
use std::path::Path;
use std::io::Write;
use std::process::{Command, Stdio};
use std::time::Duration;

use ssh_rs::ssh;
use reqwest::Client;
use serde::{Serialize, Deserialize};
use tauri::{Runtime, Window};
use pipe_downloader_lib::*;

mod mac_utils;

#[derive(Clone, Serialize)]
struct ProgressPayload {
    downloaded: usize,
    total: usize,
    num: usize,
    all: usize,
    speed: usize,
}

#[derive(Serialize, Deserialize)]
struct Config {
    ram: u32,
    cpu: u32,
}

#[tauri::command]
fn get_frame() -> String {
    let packages = mac_utils::missing_packages();
    mac_utils::load_page(packages)
}

#[tauri::command]
async fn install<R: Runtime>(window: Window<R>) -> String {
    // URLs
    let gs_img = "https://files.native.computer/groundseg-img.tar.xz";
    let qemu_bin = "https://files.native.computer/qemu-bin.tar.xz";
    let qemu_opt = "https://files.native.computer/qemu-opt.tar.xz";
    let qemu_lib = "https://files.native.computer/qemu-lib.tar.xz";
    let qemu_src = "https://files.native.computer/qemu-src.tar.xz";

    let files = [&gs_img, &qemu_bin, &qemu_opt, &qemu_lib, &qemu_src];
    let path_str = format!("{}", mac_utils::install_dir());
    let path = Path::new(&path_str);

    for (i, f) in files.iter().enumerate() {
        let dl = PipeDownloaderOptions {
            chunk_size_downloader: 50000000,
            chunk_size_decoder: 100000000,
            max_download_speed: Some(1000000000),
            force_no_chunks: false,
            download_threads: 8,
        };

        let res = dl.start_download(f, path).expect("failed to download");

        loop {
            let finished = &res.is_finished();
            let progress = &res.get_progress();

            let total = progress.total_download_size.unwrap_or(0);
            let downloaded = progress.downloaded;
            let speed = progress.current_download_speed;
            let _ = window.emit(
                "progress",
                ProgressPayload {
                    downloaded,
                    total,
                    num: i + 1,
                    all: files.len(),
                    speed: speed,
                }
            );

            if *finished { break };

            std::thread::sleep(Duration::from_millis(100));
        }
    }

    let packages = mac_utils::missing_packages();
    mac_utils::load_page(packages)
}

#[tauri::command]
async fn repair<R: Runtime>(window: Window<R>) -> String {
    // Get missing packages
    let packages = mac_utils::missing_packages();
    let mut files = vec![];

    // URLs
    let gs_img = "https://files.native.computer/groundseg-img.tar.xz";
    let qemu_bin = "https://files.native.computer/qemu-bin.tar.xz";
    let qemu_opt = "https://files.native.computer/qemu-opt.tar.xz";
    let qemu_lib = "https://files.native.computer/qemu-lib.tar.xz";
    let qemu_src = "https://files.native.computer/qemu-src.tar.xz";

    let path_str = format!("{}", mac_utils::install_dir());
    let path = Path::new(&path_str);

    for p in packages {
        println!("{}",p);
        if p == "qemu-bin" {
            files.push(&qemu_bin)
        };
        if p == "qemu-src" {
            files.push(&qemu_src)
        };
        if p == "gs-img" {
            files.push(&gs_img)
        };
        if p == "qemu-lib" {
            files.push(&qemu_lib)
        };
        if p == "qemu-opt" {
            files.push(&qemu_opt)
        };
    };

    for (i, f) in files.iter().enumerate() {
        let dl = PipeDownloaderOptions {
            chunk_size_downloader: 50000000,
            chunk_size_decoder: 100000000,
            max_download_speed: Some(1000000000),
            force_no_chunks: false,
            download_threads: 8,
        };

        let res = dl.start_download(f, path).expect("failed to download");

        loop {
            let finished = &res.is_finished();
            let progress = &res.get_progress();

            let total = progress.total_download_size.unwrap_or(0);
            let downloaded = progress.downloaded;
            let speed = progress.current_download_speed;
            let _ = window.emit(
                "progress",
                ProgressPayload {
                    downloaded,
                    total,
                    num: i + 1,
                    all: files.len(),
                    speed: speed,
                }
            );

            if *finished { break };

            std::thread::sleep(Duration::from_millis(100));
        }
    }

    let packages = mac_utils::missing_packages();
    mac_utils::load_page(packages)
}

#[tauri::command]
fn get_ram() -> String {
    let ram = mac_utils::get_config_ram();
    ram.to_string() 
}

#[tauri::command]
fn get_cpu() -> String {
    let cpu = mac_utils::get_config_cpu();
    cpu.to_string() 
}

#[tauri::command]
fn start(pwd: String,ram: u32,cpu: u32) -> String {
    // Kill previous sudo sessions
    let _ = Command::new("sudo").arg("-k").spawn().expect("sudo -k failed to execute");

    // Check if password is correct
    let mut pwd_cmd = Command::new("sudo")
        .arg("-S")
        .arg("echo")
        .arg("correct")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .expect("failed to start process");

    // Pass the password to stdin
    let mut pwd_stdin = pwd_cmd.stdin.take().unwrap();
    writeln!(pwd_stdin, "{}", &pwd).unwrap();
    drop(pwd_stdin);

    let correct = String::from("correct\n");
    let pwd_out = pwd_cmd.wait_with_output().expect("failed to wait on process");
    let pwd_str = String::from_utf8_lossy(&pwd_out.stdout);

    if correct.eq(&pwd_str) {
        // Define flags
        let qemu_bin = format!("{}/qemu-binaries/qemu-system-x86_64", mac_utils::install_dir());
        let gs_img = format!("{}/groundseg.qcow2", mac_utils::install_dir());
        let pid_file = format!("{}/pid", mac_utils::install_dir());
        let accel = "hvf";
        let ram_str = format!("{}G",ram);
        let ports: Vec<String> = (8081..8100).map(|x| format!(",hostfwd=tcp::{}-:{}", x, x)).collect();
        let ports = ports.join("");
        let nic = format!("user,hostfwd=tcp::1723-:22,hostfwd=tcp::80-:80,hostfwd=tcp::27016-:27016{}",ports);

        // Command
        let qemu_cmd = Command::new("sudo").arg(qemu_bin).arg(gs_img)
            .arg("-smp").arg(cpu.to_string()).arg("-m").arg(ram_str)
            .arg("-accel").arg(accel).arg("-cpu").arg("host")
            .arg("-nic").arg(nic).arg("-pidfile").arg(pid_file)
            .arg("-display").arg("none").arg("-daemonize")
            .spawn().expect("QEMU VM failed to start");

        // Print status
        let launched = String::from("");
        let qemu_out = qemu_cmd.wait_with_output().expect("failed to wait on process");
        let qemu_str = String::from_utf8_lossy(&qemu_out.stdout);

        if qemu_str.eq(&launched) {
            // set json values
            let file = format!("{}/settings.json", mac_utils::install_dir());
            let cfg = Config {ram: ram, cpu: cpu};
            let mut make_file = File::create(file).unwrap();
            serde_json::to_writer_pretty(&mut make_file, &cfg).unwrap();

            // switch to launching screen
            return "launching".to_string();
        }
    } 
    // Returns error by default
    "error".to_string()
}

#[tauri::command]
fn stop(pwd: String) -> String {
    // Kill previous sudo sessions
    let _ = Command::new("sudo").arg("-k").spawn().expect("sudo -k failed to execute");

    // Check if password is correct
    let mut pwd_cmd = Command::new("sudo")
        .arg("-S")
        .arg("echo")
        .arg("correct")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .expect("failed to start process");

    // Pass the password to stdin
    let mut pwd_stdin = pwd_cmd.stdin.take().unwrap();
    writeln!(pwd_stdin, "{}", &pwd).unwrap();
    drop(pwd_stdin);

    let correct = String::from("correct\n");
    let pwd_out = pwd_cmd.wait_with_output().expect("failed to wait on process");
    let pwd_str = String::from_utf8_lossy(&pwd_out.stdout);

    if correct.eq(&pwd_str) {
        // pid file location
        let pid = format!("{}/pid",mac_utils::install_dir());
        // get pid
        let pid_cmd = Command::new("sudo").arg("cat").arg(pid)
            .output().expect("failed to get PID");

        // pid
        let pid_str = String::from_utf8_lossy(&pid_cmd.stdout);
        let pid_str = pid_str.trim();

        // kill process
        let _ = Command::new("sudo").arg("kill").arg(&pid_str)
            .output().expect("failed to kill process");

        return "launcher".to_string()
    }

    // Returns error by default
    "error".to_string()
}

#[tauri::command]
fn restart(pwd: String) -> String {
    // Kill previous sudo sessions
    let _ = Command::new("sudo").arg("-k").spawn().expect("sudo -k failed to execute");

    // Check if password is correct
    let mut pwd_cmd = Command::new("sudo")
        .arg("-S")
        .arg("echo")
        .arg("correct")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .expect("failed to start process");

    // Pass the password to stdin
    let mut pwd_stdin = pwd_cmd.stdin.take().unwrap();
    writeln!(pwd_stdin, "{}", &pwd).unwrap();
    drop(pwd_stdin);

    let correct = String::from("correct\n");
    let pwd_out = pwd_cmd.wait_with_output().expect("failed to wait on process");
    let pwd_str = String::from_utf8_lossy(&pwd_out.stdout);

    if correct.eq(&pwd_str) {
        // pid file location
        let pid = format!("{}/pid",mac_utils::install_dir());
        // get pid
        let pid_cmd = Command::new("sudo").arg("cat").arg(pid)
            .output().expect("failed to get PID");

        // pid
        let pid_str = String::from_utf8_lossy(&pid_cmd.stdout);
        let pid_str = pid_str.trim();

        // kill process
        let _ = Command::new("sudo").arg("kill").arg(&pid_str)
            .output().expect("failed to kill process");

        // start groundseg again
        let qemu_bin = format!("{}/qemu-binaries/qemu-system-x86_64", mac_utils::install_dir());
        let gs_img = format!("{}/groundseg.qcow2", mac_utils::install_dir());
        let pid_file = format!("{}/pid", mac_utils::install_dir());
        let accel = "hvf";
        let ram = format!("{}G",mac_utils::get_config_ram());
        let cpu = mac_utils::get_config_cpu();
        let ports: Vec<String> = (8081..8100).map(|x| format!(",hostfwd=tcp::{}-:{}", x, x)).collect();
        let ports = ports.join("");
        let nic = format!("user,hostfwd=tcp::1723-:22,hostfwd=tcp::80-:80,hostfwd=tcp::27016-:27016{}",ports);

        // Command
        let qemu_cmd = Command::new("sudo").arg(qemu_bin).arg(gs_img)
            .arg("-smp").arg(cpu).arg("-m").arg(ram)
            .arg("-accel").arg(accel).arg("-cpu").arg("host")
            .arg("-nic").arg(nic).arg("-pidfile").arg(pid_file)
            .arg("-display").arg("none").arg("-daemonize")
            .spawn().expect("QEMU VM failed to start");

        // Print status
        let launched = String::from("");
        let qemu_out = qemu_cmd.wait_with_output().expect("failed to wait on process");
        let qemu_str = String::from_utf8_lossy(&qemu_out.stdout);

        if qemu_str.eq(&launched) {
            // switch to launching screen
            return "launching".to_string();
        }
    }

    // Returns error by default
    "error".to_string()
}

#[tauri::command]
async fn check_webui() -> String {
    let client = Client::new();
    let hostname = mac_utils::get_hostname();
    let url = format!("http://{}.local", &hostname);
    loop {
        match client.get(&url).send().await {
            Ok(response) => {
                if response.status().is_success() {
                    // Credentials
                    let username = "setname";
                    let password = "setnamepass";
                    let host = format!("{}.local:1723", &hostname);
                    let cmd = format!("sudo hostnamectl set-hostname {}", &hostname);

                    let mut session = ssh::create_session()
                        .username(&username)
                        .password(&password)
                        .connect(&host)
                        .unwrap()
                        .run_local();
                    let exec = session.open_exec().unwrap();
                    let vec: Vec<u8> = exec.send_command(&cmd).unwrap();
                    println!("{}", String::from_utf8(vec).unwrap());
                    // Close session.
                    session.close();

                    return "control".to_string()
                }
            },
            Err(_) => println!("GroundSeg has not started yet, checking again...")
        }
        std::thread::sleep(Duration::from_millis(100));
    }
}

#[tauri::command]
fn get_hostname() -> String {
    let hostname = mac_utils::get_hostname();
    let url = format!("http://{}.local", hostname);
    url
}

#[tauri::command]
fn get_max_ram() -> String {
   mac_utils::max_ram()
}

#[tauri::command]
fn get_max_cpu() -> String {
   mac_utils::max_cpu()
}

#[tauri::command]
fn reset_ram() -> String {
    mac_utils::default_ram()
}

#[tauri::command]
fn reset_cpu() -> String {
    mac_utils::default_cpu()
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
                        get_frame,get_hostname,check_webui,
                        install,start,stop,restart,repair,
                        reset_ram,get_ram,get_max_ram,
                        reset_cpu,get_cpu,get_max_cpu
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
