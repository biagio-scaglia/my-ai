import os
import sys

# Force online mode before transformers load
os.environ["HF_HUB_OFFLINE"] = "0"

import argparse
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

# Inizializzazione della console Rich
console = Console()


def load_ai_model(model_id="Qwen/Qwen2.5-Coder-1.5B-Instruct"):
    """
    Carica il modello e il tokenizer con una progress bar.
    """
    console.clear()
    console.print(
        Panel.fit(
            f"[bold blue]AI Assistant[/bold blue]\n[dim]Modello: {model_id}[/dim]",
            style="blue",
        )
    )

    tokenizer = None
    model = None
    rag = None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task1 = progress.add_task("[green]Importazione moduli...", total=None)
        # Importazioni lazy per feedback immediato
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from rag_engine import RagEngine

        progress.advance(task1)

        task2 = progress.add_task(
            f"[yellow]Caricamento LLM ({model_id})...", total=None
        )
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            # Fix per warning pad_token
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token

            model = AutoModelForCausalLM.from_pretrained(
                model_id, dtype="auto", device_map="auto"
            )
            progress.advance(task2)
        except Exception as e:
            console.print(f"[bold red]Errore caricamento modello: {e}[/bold red]")
            console.print(
                "[yellow]Esegui 'python download_models.py' se necessario.[/yellow]"
            )
            sys.exit(1)

        task3 = progress.add_task(
            "[magenta]Indicizzazione Conoscenza (RAG)...", total=None
        )
        try:
            rag = RagEngine()
            progress.advance(task3)
        except Exception as e:
            console.print(f"[bold red]Errore RAG: {e}[/bold red]")

    console.print("[bold green]Sistema pronto.[/bold green]")
    return tokenizer, model, rag


def chat_loop(tokenizer, model, rag):
    """
    Loop principale della chat.
    """
    console.clear()
    console.print(
        Panel.fit(
            "[bold blue]Assistente di Programmazione[/bold blue]\nSono pronto ad aiutarti.",
            title="AI Assistant",
        )
    )

    # System prompt professionale
    # System prompt professionale e rigoroso
    base_system_prompt = (
        "Sei un assistente tecnico senior di livello architect, specializzato in ingegneria del software, architetture scalabili e progettazione di sistemi moderni. "
        "Il tuo compito è analizzare richieste e progetti in modo rigoroso, fornendo valutazioni tecniche motivate, decisioni architetturali consapevoli e suggerimenti concreti basati su best practices reali e standard industriali. "
        "Suggerisci stack tecnologici moderni, mantenibili e adeguati al contesto, motivando sempre le scelte e indicando eventuali alternative con i relativi trade-off. "
        "Analizza i progetti software in profondità, evidenziando punti di forza, criticità, debito tecnico, rischi di scalabilità, sicurezza e manutenibilità, proponendo miglioramenti pratici e applicabili. "
        "Utilizza in modo attivo e coerente tutte le informazioni di CONTESTO fornite (CV, documenti, requisiti funzionali e non funzionali, vincoli tecnici) per personalizzare le risposte in base al livello, agli obiettivi e alle reali esigenze dell’utente. "
        "Comunica esclusivamente in italiano. Tono professionale, diretto e preciso. "
        "Sii sintetico ma completo. "
        "IMPORTANTE: Quando scrivi codice, COMMENTA SEMPRE I PASSAGGI CHIAVE IN ITALIANO. Il codice deve essere autodocumentato e didattico."
    )

    history = [{"role": "system", "content": base_system_prompt}]

    try:
        while True:
            # Input dell'utente
            try:
                user_input = Prompt.ask("\n[bold green]Tu[/bold green]")
            except KeyboardInterrupt:
                # Gestione Ctrl+C sul prompt
                console.print("\n[bold blue]Rilevato interrupt. Uscita...[/bold blue]")
                break

            if user_input.lower() in ["exit", "esci", "quit", "basta"]:
                console.print("[bold blue]Terminazione sessione.[/bold blue]")
                break

            if not user_input.strip():
                continue

            # Retrieval RAG
            with console.status(
                "[bold blue]Analisi contesto...[/bold blue]", spinner="dots"
            ):
                rag_results = rag.search(user_input)

            context_str = ""
            if rag_results:
                context_str = "\n\n=== CONTESTO RILEVANTE ===\n" + "\n---\n".join(
                    [r["text"] for r in rag_results]
                )
                console.print(f"[dim]Trovati {len(rag_results)} riferimenti.[/dim]")

            # Aggiunta contesto al messaggio utente
            full_input = user_input
            if context_str:
                full_input += context_str

            history.append({"role": "user", "content": full_input})

            # Generazione
            text = tokenizer.apply_chat_template(
                history, tokenize=False, add_generation_prompt=True
            )

            # Gestione attention mask esplicita
            model_inputs = tokenizer([text], return_tensors="pt", padding=True).to(
                model.device
            )

            with console.status(
                "[bold blue]Generazione risposta...[/bold blue]", spinner="dots"
            ):
                generated_ids = model.generate(
                    model_inputs.input_ids,
                    attention_mask=model_inputs.attention_mask,  # Fix warning
                    max_new_tokens=2048,  # Aumentato per risposte codificose
                    do_sample=True,
                    temperature=0.4,  # Molto preciso per il codice
                    pad_token_id=tokenizer.eos_token_id,
                )

                generated_ids = [
                    output_ids[len(input_ids) :]
                    for input_ids, output_ids in zip(
                        model_inputs.input_ids, generated_ids
                    )
                ]

                response = tokenizer.batch_decode(
                    generated_ids, skip_special_tokens=True
                )[0]

            history.append({"role": "assistant", "content": response})

            console.print(
                Panel(
                    Markdown(response),
                    title="[bold blue]Assistente[/bold blue]",
                    border_style="blue",
                )
            )

    except KeyboardInterrupt:
        console.print(
            "\n[bold blue]Interruzione forzata (Ctrl+C). A presto![/bold blue]"
        )
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coddy AI Assistant")
    parser.add_argument("query", nargs="*", help="Query diretta (opzionale)")
    parser.add_argument(
        "--model",
        type=str,
        default="coder",
        choices=["coder", "light"],
        help="Modello da usare: 'coder' (1.5B) o 'light' (0.5B)",
    )
    args = parser.parse_args()

    # Mappa dei modelli
    MODELS = {
        "coder": "Qwen/Qwen2.5-Coder-1.5B-Instruct",
        "light": "Qwen/Qwen2.5-0.5B-Instruct",
    }

    selected_model = MODELS[args.model]
    cli_query = " ".join(args.query) if args.query else None

    # Carica con il modello scelto
    tokenizer, model, rag = load_ai_model(selected_model)

    # Se c'è una query da riga di comando, eseguiamo solo quella
    if cli_query:
        # Simuliamo una history minima ma potente
        base_system_prompt = (
            "Sei un assistente tecnico senior livello Godmode. Rispondi in modo diretto, conciso e tecnico."
            "Parla in italiano. Fornisci codice se richiesto e COMMENTALO SEMPRE."
        )
        history = [
            {"role": "system", "content": base_system_prompt},
            {"role": "user", "content": cli_query},
        ]

        # Generazione diretta senza loop
        text = tokenizer.apply_chat_template(
            history, tokenize=False, add_generation_prompt=True
        )
        model_inputs = tokenizer([text], return_tensors="pt", padding=True).to(
            model.device
        )

        generated_ids = model.generate(
            model_inputs.input_ids,
            attention_mask=model_inputs.attention_mask,
            max_new_tokens=2048,
            do_sample=True,
            temperature=0.4,
            pad_token_id=tokenizer.eos_token_id,
        )
        response = tokenizer.batch_decode(
            generated_ids[0][len(model_inputs.input_ids[0]) :], skip_special_tokens=True
        )[0]

        # Output formattato su stdout per eventuale piping
        console.print(Markdown(response))

        sys.exit(0)

    # Altrimenti avvia il loop interattivo
    chat_loop(tokenizer, model, rag)
