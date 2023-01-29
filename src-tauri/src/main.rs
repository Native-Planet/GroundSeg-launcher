#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

mod mac_utils;

use tauri::Manager;
//use std::fs::File;
//use std::io::copy;
//use reqwest::Url;


// Learn more about Tauri commands at https://tauri.app/v1/guides/features/command

#[tauri::command]
fn get_frame() -> String {
    let packages = mac_utils::missing_packages();
    mac_utils::load_page(packages)
}

#[tauri::command]
fn install() -> String {
    //let app_handle = Manager::app_handle();
    //app.handle.emit_all("installer","yeet").;

    // hardcoded placeholders
    //let url = "http://localhost/groundseg-img.tar.xz";
    //let path = "/home/nal/gsl_files/groundseg-img.tar.xz";

    //let mut response = reqwest::get(url);
    //let mut dest = File::create(path).unwrap();
    //copy(&mut response, &mut dest).unwrap();
    //
    // get size of qemu-bin
    // get size of gs-img
    // get size of qemu-src

    // download qemu bin
    // emit download %

    // download qemu img
    // emit download %

    // download qemu src
    // emit download %

    // extract qemu bin
    // emit extract %

    // extract qemu img
    // emit extract %

    // extract qemu src
    // emit extract %

    // check if qemu-bin dir and gs.qcow2 exists
    // if no, proceed to repair screen
    // if yes, done!
    //"done".to_string()
    "launcher".to_string()
}

#[tauri::command]
fn start() -> String {
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
        .invoke_handler(tauri::generate_handler![get_frame,install,start])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
