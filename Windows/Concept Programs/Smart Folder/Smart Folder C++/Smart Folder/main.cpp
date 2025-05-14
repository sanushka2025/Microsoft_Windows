#include <windows.h>
#include <iostream>
#include <string>
#include <filesystem>
#include <unordered_map>
#include <algorithm>  // For std::transform

namespace fs = std::filesystem;

// Function to move files to the appropriate directory based on their extension
void MoveFileToFolder(const std::wstring& filePath, const std::wstring& watchDir, const std::unordered_map<std::wstring, std::wstring>& folderMap) {
    fs::path path(filePath);

    if (fs::is_directory(path)) {
        // If it's a directory, ignore it
        std::wcout << L"Ignored directory: " << path << std::endl;
        return;
    }

    std::wstring extension = path.extension().wstring();
    std::transform(extension.begin(), extension.end(), extension.begin(), ::towlower);
    std::wcout << L"Processing file: " << filePath << L" with extension: " << extension << std::endl;

    auto it = folderMap.find(extension);
    if (it != folderMap.end()) {
        fs::path destDir = fs::path(watchDir) / it->second;
        if (!fs::exists(destDir)) {
            fs::create_directory(destDir);
        }
        fs::path destPath = destDir / path.filename();
        fs::rename(path, destPath);
        std::wcout << L"Moved: " << path << L" to " << destPath << std::endl;
    } else {
        std::wcout << L"Extension not found in map: " << extension << std::endl;
    }
}

// Main function to monitor a directory and organize files
void WatchDirectory(const std::wstring& watchDir, const std::unordered_map<std::wstring, std::wstring>& folderMap) {
    HANDLE hDir = CreateFileW(
        watchDir.c_str(),
        FILE_LIST_DIRECTORY,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        NULL,
        OPEN_EXISTING,
        FILE_FLAG_BACKUP_SEMANTICS,
        NULL
    );

    if (hDir == INVALID_HANDLE_VALUE) {
        std::cerr << "Error opening directory handle." << std::endl;
        return;
    }

    char buffer[1024];
    DWORD bytesReturned;

    while (true) {
        if (ReadDirectoryChangesW(
            hDir,
            buffer,
            sizeof(buffer),
            TRUE,
            FILE_NOTIFY_CHANGE_FILE_NAME | FILE_NOTIFY_CHANGE_DIR_NAME,
            &bytesReturned,
            NULL,
            NULL
        )) {
            FILE_NOTIFY_INFORMATION* notify = reinterpret_cast<FILE_NOTIFY_INFORMATION*>(buffer);
            do {
                std::wstring fileName(notify->FileName, notify->FileNameLength / sizeof(WCHAR));
                std::wstring fullPath = fs::path(watchDir) / fileName;

                // Check if the change is within the main watched directory
                if (fs::path(fullPath).parent_path() == fs::path(watchDir)) {
                    if (notify->Action == FILE_ACTION_ADDED || notify->Action == FILE_ACTION_MODIFIED) {
                        MoveFileToFolder(fullPath, watchDir, folderMap);
                    }
                } else {
                    std::wcout << L"Ignored change in subdirectory: " << fullPath << std::endl;
                }

                notify = notify->NextEntryOffset ? reinterpret_cast<FILE_NOTIFY_INFORMATION*>(reinterpret_cast<char*>(notify) + notify->NextEntryOffset) : nullptr;
            } while (notify);
        } else {
            std::cerr << "Error reading directory changes." << std::endl;
            break;
        }
    }

    CloseHandle(hDir);
}

int main() {
    std::wstring watchDir = L"C:\\path\\to\\your\\watch_folder";  // Update this path

    // Map file extensions to their respective directories
    std::unordered_map<std::wstring, std::wstring> folderMap = {
        {L".jpg", L"Images"},
        {L".jpeg", L"Images"},
        {L".png", L"Images"},
        {L".gif", L"Images"},
        {L".pdf", L"Documents"},
        {L".docx", L"Documents"},
        {L".txt", L"Documents"},
        {L".mp4", L"Videos"},
        {L".avi", L"Videos"},
        {L".mov", L"Videos"},
        {L".mp3", L"Music"},
        {L".wav", L"Music"},
        {L".aac", L"Music"}
    };

    std::wcout << L"Watching folder: " << watchDir << std::endl;
    WatchDirectory(watchDir, folderMap);

    return 0;
}
