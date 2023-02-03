use std::fs;
use std::path::Path;
//use std::fs::file;
//use std::io::prelude::*;

//use reqwest::Client;
//use std::io::{self, Write};

pub const INSTALL_DIR : &str  = "/home/nal/gsl_files";

pub fn missing_packages() -> Vec<String> {
    let mut missing = vec![];

    // Check if INSTALL_DIR exists, if not, create it
    if !Path::new(INSTALL_DIR).exists() {
        match fs::create_dir(INSTALL_DIR) {
            Ok(_) => {}
            Err(e) => println!("Error creating INSTALL_DIR: {}", e),
        }
    }

    // Check if <INSTALL_DIR>/qemu-binaries exists, 
    // if not, append 'qemu-bin' to the missing array
    let qemu_binaries = format!("{}/qemu-binaries", INSTALL_DIR);
    if !Path::new(&qemu_binaries).exists() {
        missing.push("qemu-bin".to_string());
    }

    // Check if <INSTALL_DIR>/groundseg.qcow2 exists,
    // if not, append 'qemu-img' to the missing array
    let groundseg_qcow2 = format!("{}/groundseg.qcow2", INSTALL_DIR);
    if !Path::new(&groundseg_qcow2).exists() {
        missing.push("qemu-img".to_string());
    }

    // Check if <INSTALL_DIR>/qemu-src.tar.xz exists,
    // if not, append 'qemu-src' to the missing array
    let qemu_src_tar_xz = format!("{}/qemu-src.tar.xz", INSTALL_DIR);
    if !Path::new(&qemu_src_tar_xz).exists() {
        missing.push("qemu-src".to_string());
    }

    return missing;
}

pub fn load_page(packages: Vec<String>) -> String {
    if packages.len() == 0 {
        "launcher".to_string()
    } else if packages.len() == 3 {
        "install".to_string()
    } else if packages.len() == 1 {
        if packages.get(0).unwrap().to_string() == "qemu-src" {
            "launcher".to_string()
        } else {
            "fix".to_string()
        }
    } else {
        "fix".to_string()
    }
}

//#[derive(Serialize, Deserialize, Debug)]
//struct Person {
//    name: String,
//    age: u32,
//}

pub fn get_config_ram() -> String {
    let config = format!("{}/config.json", INSTALL_DIR);

    // Get max ram
    let max_ram = sys_info::mem_info().unwrap().total / u64::pow(2,20);
    // 80% as default
    let mut ram = (max_ram as f32 * 0.8) as u64;

    if !Path::new(&config).exists() {
        return ram.to_string()
    } else {
        // get from json
        // if value is less than max, return value from json
        // else return ram value
        return "12".to_string()
    }
}

pub fn get_config_cpu() -> String {
    let config = format!("{}/config.json", INSTALL_DIR);

    // Get max ram
    let max_cpu = sys_info::cpu_num().unwrap();
    // 80% as default
    let mut cpu = (max_cpu as f32 * 0.8) as u32;

    if !Path::new(&config).exists() {
        return cpu.to_string()
    } else {
        // get from json
        // if value is less than max, return value from json
        // else return cpu value
        return "4".to_string()
    }
}

pub fn get_hostname() -> String {
    let hostname = sys_info::hostname().unwrap();
    /*
    if hostname.ends_with(".local") {
        let mut result = hostname;
        result.push_str(".local");
        return result;
    } */
    hostname
}
//pub async fn download(url: &str) -> Result<(u64), reqwest::Error> {
//    let client = Client::new();
//    let mut res = client.get(url).send().await?;
//    while let Some(chunk) = res.chunk().await? {
//        io::stdout().write_all(&chunk)?;
//        io::stdout().flush()?;
//        println!("Received chunk of size: {}", chunk.len());
//    }
//    Ok(0)
//}
