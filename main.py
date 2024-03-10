from flask import Flask, request, render_template
import cx_Oracle

app = Flask(__name__)


# Função para realizar as atualizações no banco de dados
def executar_updates(cd_pessoa_fisica):
    # Dados de conexão ao banco de dados Oracle
    dsn_tns = cx_Oracle.makedsn('HOST', 'PORTA', service_name='NOME_DO_SERVICO')
    conn = cx_Oracle.connect(user='USUARIO', password='SENHA', dsn=dsn_tns)
    
    # Script SQL para os updates
    updates = [
        """
        update pls_segurado_carteira
        set cd_usuario_plano=(
            select pls_elimina_zeros_esquerda(b.cd_usuario_plano) mtrsemzero
            from pls_segurado a, pls_segurado_carteira b
            where a.nr_sequencia = b.nr_seq_segurado
            and a.cd_pessoa_fisica = :cd_pessoa_fisica
            and a.ie_situacao_atend in ('A', 'F')
            and a.nr_seq_plano in (3,44)
        )
        where nr_sequencia = (
            select b.nr_sequencia
            from pls_segurado a, pls_segurado_carteira b
            where a.nr_sequencia = b.nr_seq_segurado
            and a.cd_pessoa_fisica = :cd_pessoa_fisica
            and a.nr_seq_plano in (3,44)
            and a.ie_situacao_atend in ('A', 'F')
        )
        """,
        """
        update pls_segurado_carteira
        set cd_usuario_plano=(
            select '20' || pls_elimina_zeros_esquerda(b.cd_usuario_plano) mtrsemzero
            from pls_segurado a, pls_segurado_carteira b
            where a.nr_sequencia = b.nr_seq_segurado
            and a.cd_pessoa_fisica = :cd_pessoa_fisica
            and a.nr_seq_plano in (3,44)
            and a.ie_situacao_atend in ('A', 'F')
        )
        where nr_sequencia = (
            select b.nr_sequencia
            from pls_segurado a, pls_segurado_carteira b
            where a.nr_sequencia = b.nr_seq_segurado
            and a.cd_pessoa_fisica = :cd_pessoa_fisica
            and a.nr_seq_plano in (42)
            and a.ie_situacao_atend in ('A', 'F')
        )
        """,
        """
        update pls_segurado_carteira
        set cd_usuario_plano=(
            select '40' || pls_elimina_zeros_esquerda(b.cd_usuario_plano) mtrsemzero
            from pls_segurado a, pls_segurado_carteira b
            where a.nr_sequencia = b.nr_seq_segurado
            and a.cd_pessoa_fisica = :cd_pessoa_fisica
            and a.nr_seq_plano in (3,44)
            and a.ie_situacao_atend in ('A', 'F')
        )
        where nr_sequencia = (
            select b.nr_sequencia
            from pls_segurado a, pls_segurado_carteira b
            where a.nr_sequencia = b.nr_seq_segurado
            and a.cd_pessoa_fisica = :cd_pessoa_fisica
            and a.nr_seq_plano in (5)
            and a.ie_situacao_atend in ('A', 'F')
        )
        """
    ]
    
    # Executa as atualizações sequencialmente
    for sql_update in updates:
        cursor = conn.cursor()
        cursor.execute(sql_update, {'cd_pessoa_fisica': cd_pessoa_fisica})
        conn.commit()
        cursor.close()
    
    # Fecha a conexão com o banco de dados
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtém o código de pessoa física do formulário
        cd_pessoa_fisica = request.form['codigoInput']
        
        # Executa as atualizações
        executar_updates(cd_pessoa_fisica)
        
        # Redireciona para uma página de sucesso
        return render_template('success.html')
    else:
        return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)


