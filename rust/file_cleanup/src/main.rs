use file_cleanup::config::get_config;

fn main() {
    let config = get_config(
        "/home/casey/Projects/File_Cleanup/rust/file_cleanup/tests/data/test_data.toml".to_string(),
    );
    println!("{}", config);

    // for thing in config.keys() {
    //     println!("{}", thing);
    // }
}
