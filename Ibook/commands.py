import click

from Ibook.Extension import db


def register_commands(app):
    @app.cli.command()
    # @click.option('--category', default=5, help='Create fake category.')
    # @click.option('--post', default=20, help='Create fake posts.')
    # @click.option('--comment', default=500, help='Create fake comments.')
    def forge():
        """Create fake posts."""
        # from Blog.fakes import fake_post, fake_comment, fake_admin, fake_category

        db.drop_all()
        click.echo('Dropped all tables.')
        db.create_all()
        click.echo('Created tables.')


