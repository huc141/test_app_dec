const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const zlib = require('zlib');
const stream = require('stream');
const { execSync } = require('child_process');

const backupBaseDir = 'D:/1-原生-android/埋点测试/1';
// const backupBaseDir = '/Users/gilboom/code/reolink/svc-device-telemetric-collect/backups';

const privateKeyFile = 'D:/1-原生-android/埋点解密key/key.pem';
// const privateKeyFile = '/Users/gilboom/code/reolink/svc-device-telemetric-collect/.keypair/key.pem';

const privateKey = fs.readFileSync(privateKeyFile);

const recoverBackups = async () => {

    process.chdir(backupBaseDir);

    const backups = fs.readdirSync(backupBaseDir).filter(file => file.endsWith('.tar'));

    for (const i of backups) {

        console.log(`Recovering ${i}`);

        const backupDir = path.join(backupBaseDir, i.replace('.tar', ''));

        if (fs.existsSync(backupDir)) {
            console.log(`Removing existing backup directory ${backupDir}`);
            fs.rmSync(backupDir, { recursive: true, force: true });
        }

        fs.mkdirSync(backupDir);
        execSync(`tar -xf ${path.join(backupBaseDir, i)} -C ${backupDir}`);

        process.chdir(backupDir);

        console.log('Decrypting aes key');

        const encryptedKeyFile = path.join(backupDir, fs.readdirSync(backupDir).find(file => file.endsWith('.key')));

        const encryptedKey = fs.readFileSync(encryptedKeyFile);

        const keyInfo = JSON.parse(crypto.privateDecrypt({
            key: privateKey,
            padding: crypto.constants.RSA_PKCS1_PADDING,
        }, encryptedKey).toString('utf-8'));

        console.log('Decrypting file');

        const encryptedFile = path.join(backupDir, fs.readdirSync(backupDir).find(file => file.endsWith('.enc')));

        const encryptedData = fs.readFileSync(encryptedFile);

        const compressedFile = encryptedFile.replace('.enc', '');

        const originalFile = compressedFile.replace('.gz', '');

        const decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(keyInfo.key, 'hex'), Buffer.from(keyInfo.iv, 'hex'));

        await stream.promises.pipeline(
            stream.Readable.from(encryptedData),
            decipher,
            zlib.createGunzip(),
            fs.createWriteStream(originalFile),
            { end: true }
        )

        fs.renameSync(originalFile, path.join(backupBaseDir, path.basename(originalFile)));

    }
};

recoverBackups();