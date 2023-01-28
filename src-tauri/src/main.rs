#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

mod mac_utils;

// Learn more about Tauri commands at https://tauri.app/v1/guides/features/command

#[tauri::command]
fn get_page() -> String {
    let packages = mac_utils::missing_packages();
    mac_utils::load_page(packages)
}

#[tauri::command]
fn install() -> String {
    println!("install called");
    "done".to_string()
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
        .invoke_handler(tauri::generate_handler![get_page,install])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
