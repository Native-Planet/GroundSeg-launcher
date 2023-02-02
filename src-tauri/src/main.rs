#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]
extern crate sys_info;
 
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
    println!("{} {} {}", pwd,ram,cpu);
    // check if sudo password is correct
    // if yes, proceed to start qemu
    // if no:
    //"error".to_string()
    "launching".to_string()
}

#[tauri::command]
fn check_webui() -> String {
    // ping <hostname>.local
    // if false
    //"error".to_string()
    // if true
    "control".to_string()
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
                        get_frame,get_ram,get_cpu,
                        check_webui,install,start
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
