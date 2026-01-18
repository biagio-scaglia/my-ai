import os
import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live

# Force online mode before potential imports
os.environ["HF_HUB_OFFLINE"] = "0"

# Importa Engine C++ e RAG
from engine_cpp import CoddyEngine2
from rag_engine import RagEngine

# Inizializzazione della console Rich
console = Console()


def web_search(query, max_results=3):
    """
    Esegue una ricerca web anonima usando DuckDuckGo (ddgs).
    """
    try:
        from ddgs import DDGS

        results = []
        with DDGS() as ddgs_inst:
            ddgs_gen = ddgs_inst.text(query, max_results=max_results)
            for r in ddgs_gen:
                results.append(f"[Fonte Web: {r['title']}]({r['href']})\n{r['body']}")
        return results
    except Exception as e:
        console.print(f"[bold red]Errore Ricerca Web: {e}[/bold red]")
        return []


def init_system():
    """
    Inizializza i motori (RAG + Llama.cpp) con feedback visivo.
    """
    console.clear()
    console.print(
        Panel.fit(
            "[bold green]Coddy Godmode v2.0[/bold green]\n[dim]Hybrid CPU Engine (Llama.cpp + Qdrant)[/dim]",
            style="green",
        )
    )

    rag = None
    engine = None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        # 1. RAG
        task1 = progress.add_task("[magenta]Caricamento Memoria (RAG)...", total=None)
        try:
            rag = RagEngine()
            progress.advance(task1)
        except Exception as e:
            console.print(f"[bold red]Errore RAG: {e}[/bold red]")

        # 2. Engine C++
        task2 = progress.add_task(
            "[cyan]Avvio Motori Neurali (Coder + Light)...", total=None
        )
        try:
            engine = CoddyEngine2()
            engine.start()  # Carica i GGUF
            progress.advance(task2)
        except Exception as e:
            console.print(f"[bold red]Errore Engine AI: {e}[/bold red]")
            sys.exit(1)

    console.print("[bold green]Sistemi online.[/bold green]")
    return engine, rag


def chat_loop(engine, rag, enable_online=False):
    """
    Loop principale della chat con Streaming e Dynamic Brain.
    """
    console.clear()
    console.print(
        Panel.fit(
            f"[bold blue]Coddy AI v2.0[/bold blue]\n[dim]Dual Brain: AUTO[/dim]\nOnline: {'[green]ON[/green]' if enable_online else '[dim]OFF[/dim]'}",
            title="Ready",
            border_style="green",
        )
    )

    base_system_prompt = (
        "Sei Coddy, un assistente AI esperto di programmazione.\n"
        "Sei conciso, tecnico e vai dritto al punto.\n"
        "Se mostri codice, usa markdown.\n"
        "Non divagare in scuse o premesse inutili."
    )

    history = [{"role": "system", "content": base_system_prompt}]

    # Setup Live display styling
    from rich.live import Live
    from rich.markdown import Markdown

    try:
        while True:
            try:
                user_input = Prompt.ask("\n[bold green]Tu[/bold green]")
            except KeyboardInterrupt:
                console.print("\n[bold blue]Uscita...[/bold blue]")
                break

            # Comandi speciali
            if user_input.lower() in ["exit", "esci", "quit"]:
                break
            if user_input.lower() in ["cls", "clear", "pulisci"]:
                console.clear()
                console.print(
                    Panel.fit(
                        f"[bold blue]Coddy AI v2.0[/bold blue]\n[dim]Dual Brain: AUTO[/dim]\nOnline: {'[green]ON[/green]' if enable_online else '[dim]OFF[/dim]'}",
                        title="Ready",
                        border_style="green",
                    )
                )
                continue

            if not user_input.strip():
                continue

            # 1. Retrieval RAG
            rag_results = []
            with console.status("[dim]RAG Scanning...[/dim]", spinner="dots"):
                rag_results = rag.search(user_input)

            # 2. Web Search (opzionale)
            web_results = []
            if enable_online:
                with console.status("[dim]Web Search...[/dim]", spinner="earth"):
                    web_results = web_search(user_input)

            # Costruzione prompt
            context_parts = []
            if rag_results:
                context_parts.append("=== KNOWLEDGE BASE ===")
                for r in rag_results:
                    context_parts.append(f"{r['text']}")
                console.print(f"[dim]📚 RAG: {len(rag_results)} frammenti[/dim]")

            if web_results:
                context_parts.append("=== WEB RESULTS ===")
                context_parts.extend(web_results)
                console.print(f"[dim]🌐 Web: {len(web_results)} risultati[/dim]")

            full_input = user_input
            if context_parts:
                full_input += "\n\n" + "\n".join(context_parts)

            history.append({"role": "user", "content": full_input})

            # Generazione Streaming con Rich Live (Migliora stile codice)
            console.print("[bold blue]Coddy[/bold blue]:")

            current_model = engine.route_query(full_input)
            full_response = ""

            # Pannello Live che stream markdown
            with Live(Markdown(""), refresh_per_second=12, console=console) as live:
                try:
                    stream_gen = engine.stream_chat(history, model_type=current_model)
                    for chunk in stream_gen:
                        if chunk:
                            full_response += chunk
                            live.update(Markdown(full_response))
                except Exception as e:
                    console.print(f"\n[red]Errore generazione: {e}[/red]")

            # Aggiungi alla history
            history.append({"role": "assistant", "content": full_response})

    except KeyboardInterrupt:
        pass
    finally:
        # Pulizia esplicita per evitare errori __del__
        if rag:
            try:
                rag.close()
            except:
                pass
        if engine:
            try:
                engine.close()
            except:
                pass
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="*", help="One-shot query")
    parser.add_argument("--online", action="store_true", help="Abilita ricerca web")
    args = parser.parse_args()

    engine, rag = init_system()

    cli_query = " ".join(args.query) if args.query else None

    if cli_query:
        # One-shot execution
        # (Semplificato per v2 - logica simile alla chat ma singola)
        base_system_prompt = "Sei Coddy. Rispondi in modo tecnico e conciso."
        history = [{"role": "system", "content": base_system_prompt}]

        # RAG One-shot
        rag_results = rag.search(cli_query)
        context = ""
        if rag_results:
            context += "\n=== CONTEXT ===\n" + "\n".join(
                [r["text"] for r in rag_results]
            )

        if args.online:
            web = web_search(cli_query)
            if web:
                context += "\n=== WEB ===\n" + "\n".join(web)

        history.append({"role": "user", "content": cli_query + context})

        print("\n", end="")
        full_response = ""
        for chunk in engine.stream_chat(history, model_type="auto"):
            if chunk:
                print(chunk, end="", flush=True)
        print("\n")

        rag.close()
        sys.exit(0)

    # Interactive
    chat_loop(engine, rag, enable_online=args.online)
