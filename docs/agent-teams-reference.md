# Orquestre equipes de sessões Claude Code

> Coordene múltiplas instâncias Claude Code trabalhando juntas como uma equipe, com tarefas compartilhadas, mensagens entre agentes e gerenciamento centralizado.

> **Aviso:** Equipes de agentes são experimentais e desabilitadas por padrão. Ative-as adicionando `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` ao seu settings.json ou ambiente. Equipes de agentes têm limitações conhecidas em torno de retomada de sessão, coordenação de tarefas e comportamento de encerramento.

Equipes de agentes permitem que você coordene múltiplas instâncias Claude Code trabalhando juntas. Uma sessão atua como o **líder da equipe**, coordenando o trabalho, atribuindo tarefas e sintetizando resultados. Os **companheiros de equipe** trabalham independentemente, cada um em sua própria context window, e se comunicam diretamente uns com os outros.

Diferentemente de subagents, que são executados dentro de uma única sessão e podem apenas relatar de volta ao agente principal, você também pode interagir com companheiros de equipe individuais diretamente sem passar pelo líder.

> **Nota:** Equipes de agentes requerem Claude Code v2.1.32 ou posterior. Verifique sua versão com `claude --version`.

---

## Conteúdo

- [Quando usar equipes de agentes](#quando-usar-equipes-de-agentes)
- [Ativar equipes de agentes](#ativar-equipes-de-agentes)
- [Inicie sua primeira equipe de agentes](#inicie-sua-primeira-equipe-de-agentes)
- [Controle sua equipe de agentes](#controle-sua-equipe-de-agentes)
- [Como funcionam as equipes de agentes](#como-funcionam-as-equipes-de-agentes)
- [Exemplos de casos de uso](#exemplos-de-casos-de-uso)
- [Melhores práticas](#melhores-práticas)
- [Troubleshooting](#troubleshooting)
- [Limitações](#limitações)

---

## Quando usar equipes de agentes

Equipes de agentes são mais eficazes para tarefas onde a exploração paralela adiciona valor real. Os casos de uso mais fortes são:

- **Pesquisa e revisão**: múltiplos companheiros de equipe podem investigar diferentes aspectos de um problema simultaneamente, depois compartilhar e desafiar as descobertas uns dos outros
- **Novos módulos ou recursos**: companheiros de equipe podem possuir cada um uma peça separada sem se atrapalharem
- **Depuração com hipóteses concorrentes**: companheiros de equipe testam diferentes teorias em paralelo e convergem para a resposta mais rapidamente
- **Coordenação entre camadas**: mudanças que abrangem frontend, backend e testes, cada uma de propriedade de um companheiro de equipe diferente

Equipes de agentes adicionam sobrecarga de coordenação e usam significativamente mais tokens do que uma única sessão. Funcionam melhor quando os companheiros de equipe podem operar independentemente. Para tarefas sequenciais, edições no mesmo arquivo ou trabalho com muitas dependências, uma única sessão ou subagents são mais eficazes.

### Comparar com subagents

Tanto equipes de agentes quanto subagents permitem paralelizar o trabalho, mas operam de forma diferente. Escolha com base em se seus trabalhadores precisam se comunicar uns com os outros:

|                   | Subagents                                                  | Agent teams                                                       |
| :---------------- | :--------------------------------------------------------- | :---------------------------------------------------------------- |
| **Context**       | Context window própria; resultados retornam ao chamador    | Context window própria; totalmente independente                   |
| **Communication** | Relatam resultados de volta apenas ao agente principal     | Companheiros de equipe se mensageiam diretamente                  |
| **Coordination**  | Agente principal gerencia todo o trabalho                  | Lista de tarefas compartilhada com auto-coordenação               |
| **Best for**      | Tarefas focadas onde apenas o resultado importa            | Trabalho complexo que requer discussão e colaboração              |
| **Token cost**    | Menor: resultados resumidos de volta ao contexto principal | Maior: cada companheiro de equipe é uma instância Claude separada |

Use **subagents** quando você precisa de trabalhadores rápidos e focados que relatem de volta. Use **equipes de agentes** quando os companheiros de equipe precisam compartilhar descobertas, desafiar uns aos outros e coordenar por conta própria.

---

## Ativar equipes de agentes

Equipes de agentes são desabilitadas por padrão. Ative-as definindo a variável de ambiente `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` como `1`, seja no seu ambiente de shell ou através de settings.json:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

---

## Inicie sua primeira equipe de agentes

Após ativar equipes de agentes, diga ao Claude para criar uma equipe e descreva a tarefa e a estrutura desejada em linguagem natural. Claude cria a equipe, gera companheiros de equipe e coordena o trabalho com base no seu prompt.

Este exemplo funciona bem porque os três papéis são independentes e podem explorar o problema sem esperar um pelo outro:

```text
I'm designing a CLI tool that helps developers track TODO comments across
their codebase. Create an agent team to explore this from different angles: one
teammate on UX, one on technical architecture, one playing devil's advocate.
```

A partir daí, Claude cria uma equipe com uma lista de tarefas compartilhada, gera companheiros de equipe para cada perspectiva, faz com que explorem o problema, sintetiza descobertas e tenta limpar a equipe quando terminar.

O terminal do líder lista todos os companheiros de equipe e no que estão trabalhando. Use `Shift+Down` para percorrer os companheiros de equipe e envie mensagens para eles diretamente. Após o último companheiro de equipe, `Shift+Down` volta para o líder.

---

## Controle sua equipe de agentes

Diga ao líder o que você quer em linguagem natural. Ele lida com coordenação de equipe, atribuição de tarefas e delegação com base em suas instruções.

### Escolha um modo de exibição

Equipes de agentes suportam dois modos de exibição:

- **In-process**: todos os companheiros de equipe são executados dentro do seu terminal principal. Use `Shift+Down` para percorrer os companheiros de equipe e digite para enviar mensagens para eles diretamente. Funciona em qualquer terminal, nenhuma configuração extra necessária.
- **Split panes**: cada companheiro de equipe recebe seu próprio painel. Você pode ver a saída de todos de uma vez e clicar em um painel para interagir diretamente. Requer tmux ou iTerm2.

> **Nota:** `tmux` tem limitações conhecidas em certos sistemas operacionais e tradicionalmente funciona melhor no macOS. Usar `tmux -CC` no iTerm2 é o ponto de entrada sugerido.

O padrão é `"auto"`, que usa split panes se você já estiver dentro de uma sessão tmux, e in-process caso contrário. Para substituir, defina `teammateMode` no seu settings.json:

```json
{
  "teammateMode": "in-process"
}
```

Para forçar o modo in-process para uma única sessão, passe como sinalizador:

```bash
claude --teammate-mode in-process
```

**Instalação manual para split panes:**

- **tmux**: instale através do gerenciador de pacotes do seu sistema.
- **iTerm2**: instale o CLI `it2`, depois ative a API Python em iTerm2 → Settings → General → Magic → Enable Python API.

### Especifique companheiros de equipe e modelos

Claude decide o número de companheiros de equipe a gerar com base em sua tarefa, ou você pode especificar exatamente o que deseja:

```text
Create a team with 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.
```

### Exigir aprovação de plano para companheiros de equipe

Para tarefas complexas ou arriscadas, você pode exigir que os companheiros de equipe planejem antes de implementar. O companheiro de equipe trabalha em modo de plano somente leitura até que o líder aprove sua abordagem:

```text
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

Fluxo de aprovação:
1. O companheiro de equipe termina o planejamento e envia uma solicitação de aprovação ao líder.
2. O líder revisa o plano e o aprova ou rejeita com feedback.
3. Se rejeitado, o companheiro de equipe revisa com base no feedback e resubmete.
4. Uma vez aprovado, o companheiro de equipe sai do modo de plano e começa a implementação.

Para influenciar o julgamento do líder, forneça critérios no seu prompt: *"apenas aprove planos que incluam cobertura de testes"* ou *"rejeite planos que modifiquem o esquema do banco de dados"*.

### Fale com companheiros de equipe diretamente

Cada companheiro de equipe é uma sessão Claude Code completa e independente. Você pode enviar mensagens para qualquer companheiro de equipe diretamente.

- **Modo in-process**: use `Shift+Down` para percorrer os companheiros de equipe, depois digite para enviar uma mensagem. Pressione `Enter` para visualizar a sessão de um companheiro de equipe, depois `Escape` para interromper seu turno atual. Pressione `Ctrl+T` para alternar a lista de tarefas.
- **Modo split-pane**: clique em um painel de companheiro de equipe para interagir com sua sessão diretamente.

### Atribuir e reivindicar tarefas

A lista de tarefas compartilhada coordena o trabalho em toda a equipe. As tarefas têm três estados: **pendente**, **em progresso** e **concluída**. Tarefas com dependências não resolvidas não podem ser reivindicadas até que essas dependências sejam concluídas.

- **Líder atribui**: diga ao líder qual tarefa dar a qual companheiro de equipe
- **Auto-reivindicar**: após terminar uma tarefa, um companheiro de equipe pega a próxima tarefa não atribuída e desbloqueada por conta própria

A reivindicação de tarefas usa bloqueio de arquivo para evitar condições de corrida quando múltiplos companheiros de equipe tentam reivindicar a mesma tarefa simultaneamente.

### Encerrar companheiros de equipe

Para encerrar graciosamente a sessão de um companheiro de equipe:

```text
Ask the researcher teammate to shut down
```

O líder envia uma solicitação de encerramento. O companheiro de equipe pode aprovar (saindo graciosamente) ou rejeitar com uma explicação.

### Limpar a equipe

Quando você terminar, peça ao líder para limpar:

```text
Clean up the team
```

Isso remove os recursos compartilhados da equipe. Certifique-se de encerrar todos os companheiros de equipe antes de limpar.

> **Aviso:** Sempre use o líder para limpar. Os companheiros de equipe não devem executar limpeza porque seu contexto de equipe pode não ser resolvido corretamente, deixando potencialmente recursos em um estado inconsistente.

### Aplicar gates de qualidade com hooks

Use hooks para aplicar regras quando os companheiros de equipe terminam o trabalho ou as tarefas são concluídas:

- `TeammateIdle`: é executado quando um companheiro de equipe está prestes a ficar ocioso. Saia com código `2` para enviar feedback e manter o companheiro de equipe trabalhando.
- `TaskCompleted`: é executado quando uma tarefa está sendo marcada como concluída. Saia com código `2` para evitar conclusão e enviar feedback.

---

## Como funcionam as equipes de agentes

### Como Claude inicia equipes de agentes

Existem duas maneiras pelas quais as equipes de agentes começam:

- **Você solicita uma equipe**: dê ao Claude uma tarefa que se beneficie do trabalho paralelo e peça explicitamente uma equipe de agentes.
- **Claude propõe uma equipe**: se Claude determinar que sua tarefa se beneficiaria do trabalho paralelo, pode sugerir criar uma equipe. Você confirma antes que ele proceda.

Em ambos os casos, você permanece no controle. Claude não criará uma equipe sem sua aprovação.

### Arquitetura

| Componente    | Papel                                                                                               |
| :------------ | :-------------------------------------------------------------------------------------------------- |
| **Team lead** | A sessão Claude Code principal que cria a equipe, gera companheiros de equipe e coordena o trabalho |
| **Teammates** | Instâncias Claude Code separadas que cada uma trabalha em tarefas atribuídas                        |
| **Task list** | Lista compartilhada de itens de trabalho que os companheiros de equipe reivindicam e completam      |
| **Mailbox**   | Sistema de mensagens para comunicação entre agentes                                                 |

O sistema gerencia dependências de tarefas automaticamente. Quando um companheiro de equipe completa uma tarefa da qual outras dependem, as tarefas bloqueadas são desbloqueadas sem intervenção manual.

**Armazenamento local:**
- **Team config**: `~/.claude/teams/{team-name}/config.json`
- **Task list**: `~/.claude/tasks/{team-name}/`

### Permissões

Os companheiros de equipe começam com as configurações de permissão do líder. Se o líder for executado com `--dangerously-skip-permissions`, todos os companheiros de equipe também. Após gerar, você pode alterar modos de companheiros de equipe individuais, mas não pode defini-los por companheiro de equipe no tempo de geração.

### Context e comunicação

Cada companheiro de equipe tem sua própria context window. Quando gerado, um companheiro de equipe carrega o mesmo contexto de projeto que uma sessão regular: CLAUDE.md, MCP servers e skills. Ele também recebe o prompt de geração do líder. O histórico de conversa do líder **não é transferido**.

**Como os companheiros de equipe compartilham informações:**

- **Entrega automática de mensagens**: quando os companheiros de equipe enviam mensagens, elas são entregues automaticamente aos destinatários.
- **Notificações de ociosidade**: quando um companheiro de equipe termina e para, ele notifica automaticamente o líder.
- **Lista de tarefas compartilhada**: todos os agentes podem ver o status da tarefa e reivindicar trabalho disponível.

**Tipos de mensagens de companheiros de equipe:**

- `message`: envie uma mensagem para um companheiro de equipe específico
- `broadcast`: envie para todos os companheiros de equipe simultaneamente (use com moderação, pois os custos escalam com o tamanho da equipe)

### Uso de tokens

Equipes de agentes usam significativamente mais tokens do que uma única sessão. O uso de tokens escala com o número de companheiros de equipe ativos. Para tarefas rotineiras, uma única sessão é mais econômica.

---

## Exemplos de casos de uso

### Executar uma revisão de código paralela

```text
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

Cada revisor trabalha a partir do mesmo PR, mas aplica um filtro diferente. O líder sintetiza descobertas em todos os três após terminarem.

### Investigar com hipóteses concorrentes

```text
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk to
each other to try to disprove each other's theories, like a scientific
debate. Update the findings doc with whatever consensus emerges.
```

A estrutura de debate combate a ancoragem: uma vez que uma teoria é explorada, a investigação subsequente tende a ser enviesada em relação a ela. Com múltiplos investigadores independentes tentando ativamente desprovar uns aos outros, a teoria que sobrevive é muito mais provável de ser a causa raiz real.

---

## Melhores práticas

### Dê aos companheiros de equipe contexto suficiente

Os companheiros de equipe não herdam o histórico de conversa do líder. Inclua detalhes específicos da tarefa no prompt de geração:

```text
Spawn a security reviewer teammate with the prompt: "Review the authentication module
at src/auth/ for security vulnerabilities. Focus on token handling, session
management, and input validation. The app uses JWT tokens stored in
httpOnly cookies. Report any issues with severity ratings."
```

### Escolha um tamanho de equipe apropriado

- **Custos de token escalam linearmente**: cada companheiro de equipe tem sua própria context window e consome tokens independentemente.
- **Sobrecarga de coordenação aumenta**: mais companheiros de equipe significa mais comunicação e potencial para conflitos.
- **Retornos decrescentes**: além de um certo ponto, companheiros de equipe adicionais não aceleram o trabalho proporcionalmente.

**Recomendação:** comece com **3-5 companheiros de equipe** para a maioria dos fluxos de trabalho. Ter 5-6 tasks por companheiro de equipe mantém todos produtivos sem alternância de contexto excessiva.

### Dimensione tarefas apropriadamente

| Tamanho     | Problema                                                                 |
| :---------- | :----------------------------------------------------------------------- |
| Muito pequeno | Sobrecarga de coordenação excede o benefício                           |
| Muito grande  | Companheiros de equipe trabalham muito tempo sem check-ins              |
| Bem dimensionado | Unidades auto-contidas que produzem um entregável claro (uma função, um arquivo de teste, uma revisão) |

### Espere os companheiros de equipe terminarem

Se o líder começar a implementar tarefas em vez de esperar pelos companheiros de equipe:

```text
Wait for your teammates to complete their tasks before proceeding
```

### Comece com pesquisa e revisão

Se você é novo em equipes de agentes, comece com tarefas que têm limites claros e não requerem escrever código: revisar um PR, pesquisar uma biblioteca ou investigar um bug.

### Evite conflitos de arquivo

Dois companheiros de equipe editando o mesmo arquivo leva a sobrescrita. Divida o trabalho para que cada companheiro de equipe possua um conjunto diferente de arquivos.

### Monitore e direcione

Verifique o progresso dos companheiros de equipe, redirecione abordagens que não estão funcionando e sintetize descobertas conforme chegam.

---

## Troubleshooting

### Companheiros de equipe não aparecem

- No modo in-process, pressione `Shift+Down` para percorrer os companheiros de equipe ativos.
- Verifique se a tarefa era complexa o suficiente para justificar uma equipe.
- Para split panes, verifique se tmux está instalado:
  ```bash
  which tmux
  ```
- Para iTerm2, verifique se o CLI `it2` está instalado e a API Python está ativada.

### Muitos prompts de permissão

Pré-aprove operações comuns nas suas configurações de permissão antes de gerar companheiros de equipe para reduzir interrupções.

### Companheiros de equipe parando em erros

Verifique a saída usando `Shift+Down` (modo in-process) ou clicando no painel (modo split), depois:
- Dê a eles instruções adicionais diretamente
- Gere um companheiro de equipe de substituição para continuar o trabalho

### Líder encerra antes do trabalho estar pronto

Diga ao líder para continuar. Você também pode dizer ao líder para esperar os companheiros de equipe terminarem antes de prosseguir.

### Sessões tmux órfãs

```bash
tmux ls
tmux kill-session -t <session-name>
```

---

## Limitações

Equipes de agentes são experimentais. Limitações atuais:

| Limitação | Descrição |
| :-------- | :-------- |
| **Sem retomada de sessão** | `/resume` e `/rewind` não restauram companheiros de equipe in-process. Gere novos companheiros de equipe se necessário. |
| **Status da tarefa pode ficar atrasado** | Os companheiros de equipe às vezes falham em marcar tarefas como concluídas, bloqueando tarefas dependentes. Atualize o status manualmente ou solicite ao líder. |
| **Encerramento pode ser lento** | Os companheiros de equipe terminam sua solicitação atual antes de encerrar. |
| **Uma equipe por sessão** | Um líder pode gerenciar apenas uma equipe por vez. Limpe a equipe atual antes de iniciar uma nova. |
| **Sem equipes aninhadas** | Os companheiros de equipe não podem gerar suas próprias equipes. Apenas o líder pode gerenciar a equipe. |
| **Líder é fixo** | Você não pode promover um companheiro de equipe a líder ou transferir liderança. |
| **Permissões definidas no tempo de geração** | Todos os companheiros de equipe começam com o modo de permissão do líder. |
| **Split panes requerem tmux ou iTerm2** | Não suportado no terminal integrado do VS Code, Windows Terminal ou Ghostty. |

> **Dica:** `CLAUDE.md` funciona normalmente — os companheiros de equipe leem arquivos `CLAUDE.md` de seu diretório de trabalho. Use isso para fornecer orientação específica do projeto a todos os companheiros de equipe.

---

## Próximos passos

- **Delegação leve**: subagents geram agentes auxiliares para pesquisa ou verificação dentro de sua sessão — melhor para tarefas que não precisam de coordenação entre agentes.
- **Sessões paralelas manuais**: Git worktrees permitem que você execute múltiplas sessões Claude Code sem coordenação de equipe automatizada.
- **Comparar abordagens**: veja a comparação subagent vs agent team para um detalhamento lado a lado.
