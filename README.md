Gptbol 1.8
Introdução

Gptbol é uma linguagem de marcação baseada em XML, projetada para descrever operações automatizadas de modificação de arquivos de código. Essa linguagem permite realizar alterações precisas em arquivos de código-fonte de forma estruturada e controlada.
Estrutura Básica

xml

<Gptbol>
    <!-- Todas as instruções são encapsuladas dentro da tag <Gptbol> -->
    <abr cam='caminho_do_arquivo' />
    <nav tp='lin' dir='down' qt='4' />
    <mul>
        <![CDATA[
        Console.WriteLine("Linha 1 de múltiplas linhas");
        Console.WriteLine("Linha 2 de múltiplas linhas");
        Console.WriteLine("Linha 3 de múltiplas linhas");
        ]]>
    </mul>
    <sav />
</Gptbol>

Tags e Atributos
1. <Gptbol>

    Elemento raiz que contém todas as instruções
    Não possui atributos

2. <abr cam='caminho_do_arquivo' />

    Abre o arquivo que será modificado
    Atributos:
        cam: O caminho do arquivo no sistema. Utilize aspas simples para envolver o valor do atributo.
    Exemplo:

    xml

    <abr cam='c:\projetos\exemplo.py' />

3. <nav tp='...' dir='...' qt='N' />

    Move o cursor para uma posição específica no arquivo
    Atributos:
        tp: Tipo de navegação
            lin: Para navegação por linhas
            chr: Para navegação por caracteres
            bus: Para busca de texto
        dir: Direção do movimento (up, down, left, right). Omitido quando tp='bus'
        qt: Quantidade de linhas ou caracteres para mover. Omitido quando tp='bus'
        texto: Texto a ser buscado, usado apenas quando tp='bus'
    IMPORTANTE: Ao usar tp='bus', caracteres XML especiais no atributo texto devem ser escapados:
        < → &lt;
        > → &gt;
        & → &amp;
        ' → &apos;
        " → &quot;
    Exemplos:

    xml

    <nav tp='lin' dir='down' qt='4' />
    <nav tp='bus' texto='&lt;!-- Comentário HTML --&gt;' />

4. <sub old='...' new='...' />

    Substitui um trecho de código existente por um novo
    Atributos:
        old: Conteúdo atual que será substituído
        new: Novo conteúdo que será inserido no lugar do antigo
    Observação: Use aspas simples para os valores dos atributos para evitar conflitos com código contendo aspas duplas
    Exemplo:

    xml

    <sub old='x+1' new='x-1' />

5. <ins>

    Insere um novo trecho de código no ponto atual do cursor
    Conteúdo: Use <![CDATA[ ... ]]> para incluir o conteúdo
    Exemplo:

    xml

    <ins>
      <![CDATA[
      Console.WriteLine("Novo código inserido aqui.");
      ]]>
    </ins>

6. <mul>

    Insere múltiplas linhas de código no ponto atual do cursor
    Conteúdo: Use <![CDATA[ ... ]]> para incluir o conteúdo
    Exemplo:

    xml

    <mul>
      <![CDATA[
      Console.WriteLine("Linha 1 de várias linhas");
      Console.WriteLine("Linha 2 de várias linhas");
      Console.WriteLine("Linha 3 de várias linhas");
      ]]>
    </mul>

7. <rep>

    Substitui a linha atual pelo conteúdo especificado
    Conteúdo: Use <![CDATA[ ... ]]> para incluir o conteúdo
    Exemplo:

    xml

    <rep>
      <![CDATA[
      txHost.Text = this.MeuIni.ReadString(ftpAtu, "host", "");
      ]]>
    </rep>

8. <sav />

    Salva as modificações realizadas no arquivo
    Não possui atributos
    Exemplo:

    xml

    <sav />

Exemplos Completos
Exemplo 1: Inserindo código HTML com caracteres especiais

xml

<Gptbol>
    <abr cam='C:\projeto\index.html' />
    <nav tp='bus' texto='&lt;!-- Inserir aqui --&gt;' />
    <ins>
        <![CDATA[
        <div class="novo-elemento">
            <h1>Título</h1>
            <p>Conteúdo</p>
        </div>
        ]]>
    </ins>
    <sav />
</Gptbol>

Exemplo 2: Modificando múltiplas linhas

xml

<Gptbol>
    <abr cam='c:\projeto\Program.cs' />
    <nav tp='bus' texto='class Program' />
    <mul>
        <![CDATA[
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
            ProcessData();
        }
        
        static void ProcessData()
        {
            // Processamento de dados
        }
        ]]>
    </mul>
    <sav />
</Gptbol>

Considerações Importantes

    Uso de CDATA:
        Sempre use blocos <![CDATA[ ... ]]> ao inserir código que contenha caracteres especiais
        Necessário nas tags <ins>, <mul> e <rep>
    Caracteres Especiais em Atributos:
        Escape caracteres XML especiais em valores de atributos usando as entidades XML apropriadas
        Importante especialmente na tag <nav> com tp='bus'
    Aspas em Atributos:
        Use aspas simples para valores de atributos
        Facilita a inclusão de código que contenha aspas duplas
    Posicionamento do Cursor:
        Sempre verifique a posição do cursor após operações de navegação
        Use navegação por busca (tp='bus') para localização precisa

Made with
