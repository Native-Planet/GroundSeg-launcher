use std::fs;
use std::env;
use std::path::Path;

use std::fs::File;
use std::process::Command;
use std::io::Read;
use serde::{Serialize, Deserialize};

pub fn install_dir() -> String {
    let v = env::var("USER").expect("$USER is not set").to_string();
    String::from("/Users/".to_owned() + {&v} + "/Documents/groundseg")
    //String::from("/home/".to_owned() + {&v} + "/Documents/groundseg")
}

pub fn missing_packages() -> Vec<String> {
    let mut missing = vec![];

    // Check if install_dir().as_str() exists, if not, create it
    if !Path::new(install_dir().as_str()).exists() {
        match fs::create_dir(install_dir().as_str()) {
            Ok(_) => {}
            Err(e) => println!("Error creating install_dir().as_str(): {}", e),
        }
    }

    // check if qemu-binaries directory exists
    let qemu_binaries = format!("{}/qemu-binaries", install_dir().as_str());
    if !Path::new(&qemu_binaries).exists() {
        missing.push("qemu-bin".to_string());
    }

    // check if groundseg.qcow2 exists
    let groundseg_qcow2 = format!("{}/groundseg.qcow2", install_dir().as_str());
    if !Path::new(&groundseg_qcow2).exists() {
        missing.push("gs-img".to_string());
    }

    // check if qemu source code exists
    let qemu_src_tar_xz = format!("{}/qemu-7.2.0", install_dir().as_str());
    if !Path::new(&qemu_src_tar_xz).exists() {
        missing.push("qemu-src".to_string());
    }

    // check if qemu libraries exists
    let qemu_lib_tar_xz = format!("{}/lib", install_dir().as_str());
    if !Path::new(&qemu_lib_tar_xz).exists() {
        missing.push("qemu-lib".to_string());
    }
    return missing;
}

pub fn load_page(packages: Vec<String>) -> String {
    // If qemu pid file exists
    let pid_file = format!("{}/pid", install_dir().as_str());
    if Path::new(&pid_file).exists() {
        return "control".to_string();
    }

    // If qemu pid file doesn't exist
    if packages.len() == 0 {
        make_symlink();
        "launcher".to_string()
    } else if packages.len() == 4 {
        "install".to_string()
    } else if packages.len() == 1 {
        if packages.get(0).unwrap().to_string() == "qemu-src" {
            make_symlink();
            "launcher".to_string()
        } else {
            "fix".to_string()
        }
    } else {
        "fix".to_string()
    }
}

fn make_symlink() {
    // pixman
    let pixman_file = "/usr/local/opt/pixman/lib/libpixman-1.0.dylib";
    let pixman_src = format!("{}/lib/pixman", install_dir().as_str());
    let pixman_dest = "/usr/local/opt/pixman";

    if !Path::new(&pixman_file).exists() {
        let _ = Command::new("ln")
            .arg("-s")
            .arg(pixman_src) 
            .arg(pixman_dest)
            .spawn()
            .expect("failed to create pixman symlink");
    }

    // glib
    let glib_file = "/usr/local/opt/glib/lib/libgio-2.0.0.dylib";
    let glib_src = format!("{}/lib/glib", install_dir().as_str());
    let glib_dest = "/usr/local/opt/glib";

    if !Path::new(&glib_file).exists() {
        let _ = Command::new("ln")
            .arg("-s")
            .arg(glib_src) 
            .arg(glib_dest)
            .spawn()
            .expect("failed to create glib symlink");
    }

    // libslirp
    let libslirp_file = "/usr/local/opt/libslirp/lib/libslirp.0.dylib";
    let libslirp_src = format!("{}/lib/libslirp", install_dir().as_str());
    let libslirp_dest = "/usr/local/opt/libslirp";

    if !Path::new(&libslirp_file).exists() {
        let _ = Command::new("ln")
            .arg("-s")
            .arg(libslirp_src) 
            .arg(libslirp_dest)
            .spawn()
            .expect("failed to create libslirp symlink");
    }

    // libssh
    let libssh_file = "/usr/local/opt/libssh/lib/libssh.4.dylib";
    let libssh_src = format!("{}/lib/libssh", install_dir().as_str());
    let libssh_dest = "/usr/local/opt/libssh";

    if !Path::new(&libssh_file).exists() {
        let _ = Command::new("ln")
            .arg("-s")
            .arg(libssh_src) 
            .arg(libssh_dest)
            .spawn()
            .expect("failed to create libssh symlink");
    }
}

#[derive(Serialize, Deserialize)]
struct Config {
    ram: u32,
    cpu: u32,
}

pub fn get_config_ram() -> String {
    let config = format!("{}/settings.json", install_dir().as_str());

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
    let config = format!("{}/settings.json", install_dir().as_str());

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
