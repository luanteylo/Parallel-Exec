# Parallel Exec

Execução paralela de uma lista de comandos passada em [setup.txt](https://github.com/luanteylo/Parallel-Exec/blob/master/setup.txt). O programa cria um _pool_ de _threads_ e distribui a sequência de comandos nessas _threads_.

## Utilização

Para utilizar o programa basta alterar o arquivo de [setup](https://github.com/luanteylo/Parallel-Exec/blob/master/setup.txt) com os comandos desejados. 

### Variáveis do [setup.txt]

1. `EXEC_DIR=/your/program/dir` : diretório de execução
2. `OUTPUT_DIR=/your/output/dir` : diretório de saída
3. `OUTPUT_FILE=output_file` : arquivo(s) de saída
4. `ONE_OUTPUT_FILE=0` : 0 = um único arquivo para saída; 1 = um arquivo por comando
5. `N_PROC=0` : Número de threads criadas. Se N_PROC = 0, serão criadas 1 thread por cor.
6. `N_CMD=3` : Número total de comandos 
7. `N_REEXEC=1` : Número de execuções por comando.
8. `MAIL_FLAG=True` : __Feature futura__



## Versioning

versão 1.0 - 2017.

## Author

* **Luan Teylo** - *Desenvolvimento* 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details



