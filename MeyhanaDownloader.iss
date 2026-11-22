#define MyAppName "MeyhanaDownloader"
#define MyAppVersion "0.2.1"
#define MyAppPublisher "alichX"
#define MyAppExeName "MeyhanaDownloader.exe"

[Setup]
AppId={{B5C6D5AC-42A8-4E9D-B8A4-7C6B7D7A8E21}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
OutputDir=installer
OutputBaseFilename=MeyhanaDownloader-Setup-0.2.1
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "downloadffmpeg"; Description: "Скачать FFmpeg вместе с приложением"
Name: "desktopicon"; Description: "Создать ярлык на рабочем столе"

[Files]
Source: "dist\MeyhanaDownloader.exe"; DestDir: "{app}"; DestName: "{#MyAppExeName}"; Flags: ignoreversion
Source: "scripts\download_ffmpeg.ps1"; DestDir: "{app}\scripts"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -File ""{app}\scripts\download_ffmpeg.ps1"" -TargetDir ""{app}"""; Flags: runhidden waituntilterminated; StatusMsg: "Скачивание FFmpeg..."; Tasks: downloadffmpeg
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
