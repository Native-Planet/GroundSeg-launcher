#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]
extern crate sys_info;
use std::process::{Command, Stdio};
use std::io::prelude::*; 
use reqwest::Client;
use std::time::Duration;

mod mac_utils;

//use futures_util::TryStreamExt;
use serde::Serialize;
use tauri::{Runtime, Window};
//use tokio::{fs::File, io::AsyncWriteExt};
//use tokio_util::codec::{BytesCodec, FramedRead};

//use read_progress_stream::ReadProgressStream;

#[derive(Clone, Serialize)]
struct ProgressPayload {
    //id: u32,
    //progress: u64,
    total: u64,
}

#[tauri::command]
fn get_frame() -> String {
    let packages = mac_utils::missing_packages();
    mac_utils::load_page(packages)
}

#[tauri::command]
async fn install<R: Runtime>(window: Window<R>) -> String {
    let url = "http://localhost/groundseg-img.tar.xz";
    //let res = mac_utils::download(url);
    //let printed = res.await.unwrap() as u64;
    //println!("{}", printed);

    //let file_path = "/home/nal/gsl_files";
    let client = reqwest::Client::new();

    let request = client.get(url);

    let response = request.send().await.unwrap();
    let total = response.content_length().ok_or_else(|| {
        println!("Errorrrr")
    });

    //let mut file = File::create(file_path).await.unwrap();
    //let mut stream = response.bytes_stream();

    let _ = window.emit(
        "progress",
        ProgressPayload {
            total: total.unwrap() as u64
        });

    //while let Some(chunk) = stream.try_next().await.unwrap() {
    //    file.write_all(&chunk).await.unwrap();
    //    let _ = window.emit(
    //        "progress",
    //        ProgressPayload {
    //            progress: chunk.len() as u64,
    //            total,
    //        },
    //    );
    //}

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
    let url = format!("http://{}.local", hostname);
    loop {
        match client.get(&url).send().await {
            Ok(response) => {
                if response.status().is_success() {
                    // ssh here
                    return "control".to_string()
                }
            },
            Err(_) => println!("ping errored")
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

fn main() {
    //let os = std::env::consts::OS;
    //if os == "windows" {
    //    println!("Running on Windows!");
        // start windows checker
    //} else if os == "macos" {
    //    println!("Running on macOS!");
        // start macos checker
    //} else {
        // temp, move this to macos later
    //    let packages = mac_utils::missing_packages();
    //}
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
                        get_frame,get_ram,get_cpu,get_hostname,
                        check_webui,install,start
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
