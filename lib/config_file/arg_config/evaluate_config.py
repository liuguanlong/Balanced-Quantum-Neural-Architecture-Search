import os
import argparse


def get_evaluate_config():
    parser = argparse.ArgumentParser(description="Evaluating configuration")
    # Search config
    parser.add_argument(
        "--search-strategy",
        type=str,
        default="evolution",
        help="The way to search the best architecture[evolution, random_search, differentiable]")
    parser.add_argument(
        "--info-metric",
        type=str,
        default="param",
        help="HC objective for searching")

    # Supernet config
    parser.add_argument(
        "--search-space",
        type=str,
        default="proxylessnas",
        help="Search spcae in different paper [proxylessnas, fbnet_s, fbnet_l, spos]")

    # Evaluate training config
    parser.add_argument("--epochs", type=int, default=800,
                        help="The epochs for supernet training")

    parser.add_argument(
        "--optimizer",
        type=str,
        default="sgd",
        help="Optimizer for supernet training")
    parser.add_argument("--lr", type=float, default=0.045)
    parser.add_argument("--weight-decay", type=float, default=0.0004)
    parser.add_argument("--momentum", type=float, default=0.9)

    parser.add_argument("--lr-scheduler", type=str, default="cosine")
    parser.add_argument("--decay-step", type=int,default=20)
    parser.add_argument("--decay-ratio", type=float,default=0.8)

    parser.add_argument("--alpha", type=float)
    parser.add_argument("--beta", type=float)
    parser.add_argument(
        "--bn-track-running-stats",
        type=int,
        default=1,
        help="Track running stats")

    return parser
