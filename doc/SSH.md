# Generate an SSH Key Pair

1) Run the ``ssh-keygen`` command. You can use the ``-t`` option to specify the type of key to create. For example, to create an RSA key, run:
    ```bash
    ssh-keygen -t rsa
    ```

2) **Optional:** You can use the ``-b`` option to specify the length (bit size) of the key, as shown in the following example:
    ```
    ssh-keygen -b 2048 -t rsa
    ```

3) The command prompts you to enter the path to the file in which you want to save the key. A default path and file name are suggested in parentheses. For example: ``/home/user_name/.ssh/id_rsa``. To accept the default path and file name, press Enter. Otherwise, enter the required path and file name, and then press Enter.

4) The command prompts you to enter a passphrase. The passphrase is not mandatory.

5) The command generates an SSH key pair consisting of a public key and a private key, and saves them in the specified path. The file name of the public key is created automatically by appending ``.pub`` to the name of the private key file. For example, if the file name of the SSH private key is ``id_rsa``, the file name of the public key would be ``id_rsa.pub``.