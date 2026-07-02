import argparse
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import os

# Adjust pathing if ran directly
sys.path.append(os.path.join(os.path.dirname(__file__), "trading_bot"))
from bot.logging_config import setup_logging, logger
from bot.orders import OrderManager

console = Console()

def run_cli():
    setup_logging()
    
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Execution Tool")
    parser.add_argument("--symbol", type=str, required=True, help="Trading Pair (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, required=True, choices=["BUY", "SELL"], help="Order Direction")
    parser.add_argument("--type", type=str, required=True, choices=["MARKET", "LIMIT"], help="Order Execution Type")
    parser.add_argument("--qty", type=float, required=True, help="Asset execution quantity")
    parser.add_argument("--price", type=float, required=False, help="Target Price (Required for LIMIT orders)")

    args = parser.parse_args()

    # Rich Visual - Order Summary Panel
    console.print(Panel(
        f"[bold blue]Processing Order Request...[/bold blue]\n"
        f"Pair: [cyan]{args.symbol.upper()}[/cyan] | "
        f"Side: [yellow]{args.side.upper()}[/yellow] | "
        f"Type: [magenta]{args.type.upper()}[/magenta] | "
        f"Qty: {args.qty} | "
        f"Price: {args.price if args.price else 'N/A'}",
        title="[bold white]Order Intent Summary[/bold white]"
    ))

    try:
        manager = OrderManager()
        response = manager.execute(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.qty,
            price=args.price
        )
        
        # Display response table on success
        table = Table(title="Execution Confirmation Receipts", show_header=True, header_style="bold green")
        table.add_column("Metric Field", style="dim")
        table.add_column("Value Outcome")
        
        table.add_row("Status", str(response.get("status")))
        table.add_row("Order ID", str(response.get("orderId")))
        table.add_row("Executed Qty", str(response.get("executedQty")))
        table.add_row("Avg Price", str(response.get("avgPrice", "N/A")))
        
        console.print(table)
        console.print("[bold green]Success: Transaction successfully settled on Testnet engine.[/bold green]")

    except Exception as e:
        console.print(f"\n[bold red]x Order Execution Failed![/bold red]")
        console.print(f"[red]Reason Details: {str(e)}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    run_cli()