#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

extern crate sys_info;

use std::io::prelude::*;
use std::net::{TcpStream};
use ssh2::Session;use std::process::{Command, Stdio};
use reqwest::Client;
use std::time::Duration;
use std::fs::File;
use std::io::Write;
use serde::{Serialize, Deserialize};
use tauri::{Runtime, Window};

mod mac_utils;

#[derive(Clone, Serialize)]
struct ProgressPayload {
    //id: u32,
    //progress: u64,
    total: u64,
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
    // todo: make it actually work
    "launcher".to_string()
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
        let qemu_bin = format!("{}/qemu-binaries/qemu-system-x86_64", mac_utils::INSTALL_DIR);
        let gs_img = format!("{}/groundseg.qcow2", mac_utils::INSTALL_DIR);
        let pid_file = format!("{}/pid", mac_utils::INSTALL_DIR);
        let accel = "kvm" /* "hvf" */;
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
            let file = format!("{}/settings.json", mac_utils::INSTALL_DIR);
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
        let pid = format!("{}/pid",mac_utils::INSTALL_DIR);
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
        let pid = format!("{}/pid",mac_utils::INSTALL_DIR);
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
        let qemu_bin = format!("{}/qemu-binaries/qemu-system-x86_64", mac_utils::INSTALL_DIR);
        let gs_img = format!("{}/groundseg.qcow2", mac_utils::INSTALL_DIR);
        let pid_file = format!("{}/pid", mac_utils::INSTALL_DIR);
        let accel = "kvm" /* "hvf" */;
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
                    let username = "setname";
                    let password = "setnamepass";
                    let host = format!("{}.local:1723", &hostname);
                    let cmd = format!("sudo hostnamectl set-hostname {}", &hostname);

                    // Connect to the local SSH server
                    let tcp = TcpStream::connect(host).unwrap();
                    let mut sess = Session::new().unwrap();
                    sess.set_tcp_stream(tcp);
                    sess.handshake().unwrap();
                    sess.userauth_password(username,password).unwrap();

                    let mut channel = sess.channel_session().unwrap();
                    channel.exec(&cmd).unwrap();
                    let mut s = String::new();
                    channel.read_to_string(&mut s).unwrap();
                    println!("{}", s);
                    channel.wait_close();
                    println!("{}", channel.exit_status().unwrap());

                    return "control".to_string()
                }
            },
            Err(_) => println!("GroundSeg has not started yet, checking again...")
        }
        std::thread::sleep(Duration::from_secs(1));
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
                        get_frame,get_hostname,
                        check_webui,install,start,stop,restart,
                        reset_ram,get_ram,get_max_ram,
                        reset_cpu,get_cpu,get_max_cpu
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
