use std::fs;
use std::path::Path;

const INSTALL_DIR : &str  = "/home/nal/gsl_files";

pub fn missing_packages() -> Vec<String> {
    let mut missing = vec![];

    // Check if INSTALL_DIR exists, if not, create it
    if !Path::new(INSTALL_DIR).exists() {
        match fs::create_dir(INSTALL_DIR) {
            Ok(_) => {}
            Err(e) => println!("Error creating INSTALL_DIR: {}", e),
        }
    }

    // Check if <INSTALL_DIR>/qemu-binaries exists, if not, append 'qemu-bin' to the missing array
    let qemu_binaries = format!("{}/qemu-binaries", INSTALL_DIR);
    if !Path::new(&qemu_binaries).exists() {
        missing.push("qemu-bin".to_string());
    }

    // Check if <INSTALL_DIR>/groundseg.qcow2 exists, if not, append 'qemu-img' to the missing array
    let groundseg_qcow2 = format!("{}/groundseg.qcow2", INSTALL_DIR);
    if !Path::new(&groundseg_qcow2).exists() {
        missing.push("qemu-img".to_string());
    }

    // Check if <INSTALL_DIR>/qemu-src.tar.xz exists, if not, append 'qemu-src' to the missing array
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
