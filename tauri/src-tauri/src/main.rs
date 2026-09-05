// 桌宠 Tauri 主程序：创建透明置顶窗口，启动时放到屏幕右上角
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::Manager;

// 右键退出命令
#[tauri::command]
fn quit(app: tauri::AppHandle) {
    app.exit(0);
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![quit])
        .setup(|app| {
            let window = app.get_webview_window("main").expect("main window missing");

            // 放到主屏幕右上角
            let monitor = match window.current_monitor() {
                Ok(Some(m)) => Some(m),
                _ => window.primary_monitor().ok().flatten(),
            };
            if let Some(m) = monitor {
                let msize = m.size();
                let wsize = window
                    .outer_size()
                    .unwrap_or(tauri::PhysicalSize::new(200, 210));
                let x = (msize.width as i32 - wsize.width as i32 - 80).max(0);
                let y = 80;
                let _ = window.set_position(tauri::PhysicalPosition::new(x, y));
            }
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
