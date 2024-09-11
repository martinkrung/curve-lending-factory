import os
import click

from ape import project

from ape.cli import ConnectedProviderCommand, account_option

# SOME_ENV_VAR = os.getenv('SOME_ENV_VAR')

@click.group()
def cli():
    pass

@click.command(cls=ConnectedProviderCommand)
@account_option()
def info(ecosystem, provider, account, network):
    click.echo(f"ecosystem: {ecosystem.name}")
    click.echo(f"network: {network.name}")
    click.echo(f"provider_id: {provider.chain_id}")
    click.echo(f"connected: {provider.is_connected}")
    click.echo(f"account: {account}")


@click.command(cls=ConnectedProviderCommand)
@account_option()
def deploy(network, provider, account):

    arg1 = "0x4259F04C42a2CEB0183C35B239C5C5BF6570b1C4"

    deploy = account.deploy(project.PlaceHolder, arg1,  max_priority_fee="1000 wei", max_fee="0.1 gwei", gas_limit="400000")

cli.add_command(info)
cli.add_command(deploy)