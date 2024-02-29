use toml::value::Array;
use toml::Table;

enum TableOrArray {
    Table(Table),
    Array(Array),
}

struct Move {
    // copy is the same
    destination: String,
    path: Option<String>,
    time: Option<Table>,
    filetypes: Option<Array>,
    r#match: Option<String>,
    include: Option<Include>,
    exclude: Option<Exclude>,
}

struct Delete {
    path: Option<String>,
    time: Option<Table>,
    include: Option<Include>,
    exclude: Option<Exclude>,
}

struct Include {
    filetypes: Option<Array>,
    r#match: Option<String>,
}

struct Exclude {
    filetypes: Option<Array>,
    r#match: Option<String>,
}

struct DirectoryConfig {
    path: String,
    destination: String,
    time: Table,
    filetypes: Array,
    regex: Array,
    r#move: Option<TableOrArray>,
    copy: Option<TableOrArray>,
    delete: Option<TableOrArray>,
}

pub fn get_config(config_file: String) -> Table {
    let path = std::path::Path::new(&config_file);
    let config_string = match std::fs::read_to_string(path) {
        Ok(result) => result,
        Err(e) => panic!("Failed to read file: {}", e),
    };
    let config: Table = config_string.parse().unwrap();
    config
}
