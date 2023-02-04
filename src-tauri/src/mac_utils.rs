use std::fs;
use std::path::Path;

use std::fs::File;
use std::io::Read;
use serde::{Serialize, Deserialize};

// todo: replace this with a function
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

    // check if qemu-binaries directory exists
    let qemu_binaries = format!("{}/qemu-binaries", INSTALL_DIR);
    if !Path::new(&qemu_binaries).exists() {
        missing.push("qemu-bin".to_string());
    }

    // check if groundseg.qcow2 exists
    let groundseg_qcow2 = format!("{}/groundseg.qcow2", INSTALL_DIR);
    if !Path::new(&groundseg_qcow2).exists() {
        missing.push("qemu-img".to_string());
    }

    // check if qemu source code exists
    let qemu_src_tar_xz = format!("{}/qemu-src.tar.xz", INSTALL_DIR);
    if !Path::new(&qemu_src_tar_xz).exists() {
        missing.push("qemu-src".to_string());
    }

    return missing;
}

pub fn load_page(packages: Vec<String>) -> String {
    // If qemu pid file exists
    let pid_file = format!("{}/pid", INSTALL_DIR);
    if Path::new(&pid_file).exists() {
        return "control".to_string();
    }

    // If qemu pid file doesn't exist
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

#[derive(Serialize, Deserialize)]
struct Config {
    ram: u32,
    cpu: u32,
}

pub fn get_config_ram() -> String {
    let config = format!("{}/settings.json", INSTALL_DIR);

    // Get max ram
    let max_ram = sys_info::mem_info().unwrap().total / u64::pow(2,20);
    // 80% as default
    let ram = (max_ram as f32 * 0.8) as u64;

    if !Path::new(&config).exists() {
        return ram.to_string()
    } else {
        let mut file = File::open(&config).unwrap();
        let mut contents = String::new();
        file.read_to_string(&mut contents).unwrap();

        let cfg: Config = serde_json::from_str(&contents).unwrap();
        return cfg.ram.to_string()
    }
}

pub fn get_config_cpu() -> String {
    let config = format!("{}/settings.json", INSTALL_DIR);

    // Get max ram
    let max_cpu = sys_info::cpu_num().unwrap();
    // 80% as default
    let cpu = (max_cpu as f32 * 0.8) as u32;

    if !Path::new(&config).exists() {
        return cpu.to_string()
    } else {
        let mut file = File::open(&config).unwrap();
        let mut contents = String::new();
        file.read_to_string(&mut contents).unwrap();

        let cfg: Config = serde_json::from_str(&contents).unwrap();
        return cfg.cpu.to_string()
    }
}

pub fn max_ram() -> String {
    let max_ram = sys_info::mem_info().unwrap().total / u64::pow(2,20);
    max_ram.to_string()
}

pub fn max_cpu() -> String {
    let max_cpu = sys_info::cpu_num().unwrap();
    max_cpu.to_string()
}

pub fn default_ram() -> String {
    // Get max ram
    let max_ram = sys_info::mem_info().unwrap().total / u64::pow(2,20);
    // 80% as default
    let ram = (max_ram as f32 * 0.8) as u64;
    ram.to_string()
}

pub fn default_cpu() -> String {
    // Get max cpu
    let max_cpu = sys_info::cpu_num().unwrap();
    // 80% as default
    let cpu = (max_cpu as f32 * 0.8) as u32;
    cpu.to_string()
}

pub fn get_hostname() -> String {
    let mut hostname = sys_info::hostname().unwrap();
    if hostname.ends_with(".local") {
        let new_len = hostname.len() - ".local".len();
        hostname.truncate(new_len)
    }
    hostname
}
