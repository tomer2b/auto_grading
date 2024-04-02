$url_vscode = "https://vscode.download.prss.microsoft.com/dbazure/download/stable/0ee08df0cf4527e40edc9aa28f4b5bd38bbff2b2/VSCodeSetup-x64-1.85.1.exe"
$vscode_dest = "C:\temp\VSCodeSetup-x64-1.85.1.exe"
$url_git = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
$git_dest = "Git-2.43.0-64-bit.exe"

$vscode_user_install_path="$Env:USERPROFILE\appdata\local\Programs\Microsoft VS Code\code.exe"
$vscode_machine_install_path="C:\Program Files\Microsoft VS Code\code.exe"

$flag_install_vscode = $true
$flag_install_git = $true
$flag_install_extension = $true

try {
	if (Get-Command git.exe -ErrorAction SilentlyContinue) {
		Write-Host "Git is installed."
	} else {
		Write-Host "Downloading Git..."
		Invoke-RestMethod -Uri $url_git -OutFile $git_dest
		Write-Host "Finished Download."
		
		Write-Host "Git is not installed. Installing it ..."
		Start-Process -FilePath $git_dest -Argument "/VERYSILENT /NORESTART"
		Write-Host "install finished"
		
	}
}
catch {
		$flag_install_git = $false
		Write-Host "Problem occured while installing Git , Please contact Tomer"	
		exit
}


try {
	if ((Get-Command $vscode_user_install_path -ErrorAction SilentlyContinue) -or (Get-Command $vscode_machine_install_path -ErrorAction SilentlyContinue)) {
		Write-Host "Visual Studio Code is installed."

	}	
	else {
		Write-Host "Downloading Vscode..."
		Invoke-RestMethod -Uri $url_vscode -OutFile $vscode_dest
		Write-Host "Finished Download."
		
		Write-Host "Visual Studio Code is not installed. Installing it ..."
		Start-Process -FilePath $vscode_dest -Argument "/VERYSILENT /NORESTART /MERGETASKS=!runcode,desktopicon,addcontextmenufiles,addcontextmenufolders"
		Write-Host "install finished"
	}	

}
catch {
		$flag_install_vscode = $false
		Write-Host "Vscode Problem , Please contact Tomer"	
		exit
}


try {
	Write-Host "Installing extenstions..."
	code --install-extension "GitHub.vscode-pull-request-github"
	code --install-extension "ms-python.python"
	code --install-extension "emeraldwalk.RunOnSave"
	code --install-extension "donjayamanne.githistory"
	code --install-extension "Dart-Code.flutter"
	code --install-extension "Dart-Code.dart-code"

}
catch {
	$flag_install_extension = $false
	Write-Host "Vscode extension Problem , Please contact Tomer"	
	exit
}


$url = "https://raw.githubusercontent.com/RabinSchool/python_examples/main/settings.json"

$dest = "$Env:USERPROFILE\appdata\Roaming\code\user\settings.json"
$bkpdest = "$Env:USERPROFILE\appdata\Roaming\code\user\settings_bkp.json"	



if ($flag_install_vscode -eq $true -and
	$flag_install_git -eq $true -and
	$flag_install_extension -eq $true){
	
	if (Test-Path $dest) {
		if (-not (Test-Path $bkpdest)){
			Write-Host "Backing up settings.json" 
			Rename-Item -Path $dest -NewName $bkpdest
		}
	}

	try {
		Write-Host "Downloading settings.json" 
		Invoke-RestMethod -Uri $url -OutFile $dest
		#$userName = Read-Host "Enter your name:"
		#$userLocation = Read-Host "Enter your email ,(on lab install write auto):"
		git config --global --add safe.directory *
		git config --global user.name "AutoInstall"
		git config --global user.email "auto.install@cs.com"

		Write-Host "Installation finished succefuly"
	}
	catch {
		Write-Host "VSCode settings Problem , Please contact Tomer"	
		exit
	}
}



Pause





# studio.exe --silent --all-users --install-location=C:\Your\Installation\Path --accept-license
