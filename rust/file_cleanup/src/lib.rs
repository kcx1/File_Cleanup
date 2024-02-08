use std::fs;
use std::time::SystemTime;

fn current_time() -> SystemTime {
    SystemTime::now()
}

fn last_accessed(path: &str) -> SystemTime {
    //TODO:  Don't use unwrap
    fs::metadata(path).unwrap().accessed().unwrap()
}

pub fn is_expired(file_name: &str) -> bool {
    current_time() > last_accessed(file_name)
}

pub fn minutes(num_of_mins: i32) -> i32 {
    num_of_mins * 60
}

pub fn hours(num_of_hours: i32) -> i32 {
    minutes(60) * num_of_hours
}

pub fn days(num_of_days: i32) -> i32 {
    hours(24) * num_of_days
}
