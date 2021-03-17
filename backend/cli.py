import click


@click.command("pip-compile",
               context_settings=dict(
                   ignore_unknown_options=True,
                   allow_extra_args=True,
                   help_option_names=[]))
@click.pass_context
def pip_compile(ctx: click.Context):
    """Compile the .in files in /requirements.

    This command is for development purposes only.
    """
    import subprocess
    if len(ctx.args) == 1 and ctx.args[0] == "--help":
        subprocess.call(["pip-compile", "--help"])
    else:
        subprocess.call(["pip-compile", "requirements/dev_unix.in", *ctx.args])
        subprocess.call(["pip-compile", "requirements/dev_windows.in",
                         *ctx.args])
        subprocess.call(["pip-compile", "requirements/prod.in", *ctx.args])
        subprocess.call(["pip-compile", "requirements/docs.in", *ctx.args])
