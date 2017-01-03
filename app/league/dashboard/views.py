# -*- coding: utf-8 -*-
"""Dashboard."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from league.dashboard.forms import (GameCreateForm, GameDeleteForm,
                                    PlayerCreateForm, PlayerDeleteForm,
                                    ReportGenerateForm)
from league.dashboard.models import Game, Player
from league.dashboard.reports import Report
from league.utils import flash_errors

blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard',
                      static_folder='../static')


@blueprint.route('/')
@login_required
def dashboard():
    """Dashboard."""
    players = Player.query.all()
    return render_template('dashboard/dashboard.html', players=players)


@blueprint.route('/players/', methods=['GET'])
@login_required
def get_players():
    """Get list of players."""
    form = PlayerCreateForm(request.form, csrf_enabled=False)
    players = Player.query.all()
    return render_template('dashboard/players.html', players=players,
                           player_create_form=form)


@blueprint.route('/players/', methods=['POST'])
@login_required
def create_player():
    """Create a new player."""
    form = PlayerCreateForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        Player.create(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            aga_id=form.aga_id.data,
            aga_rank=form.aga_rank.data
        )
        flash('Player created!', 'success')
    else:
        flash_errors(form)
    players = Player.query.all()
    return render_template('dashboard/players.html', players=players,
                           player_create_form=form)


@blueprint.route('/players/delete/', methods=['POST'])
@login_required
def delete_player():
    """Delete a player."""
    form = PlayerDeleteForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        Player.delete(Player.get_by_id(form.player_id.data))
        flash('Player deleted!', 'success')
    else:
        flash_errors(form)
    return redirect(url_for('dashboard.get_players'))


@blueprint.route('/games/', methods=['GET'])
@login_required
def get_games():
    """Get list of games."""
    form = GameCreateForm(request.form, csrf_enabled=False)
    games = Game.query.all()
    return render_template('dashboard/games.html', games=games,
                           game_create_form=form)


@blueprint.route('/games/', methods=['POST'])
@login_required
def create_game():
    """Create a new game."""
    form = GameCreateForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        white = Player.get_by_aga_id(form.white_id.data)
        black = Player.get_by_aga_id(form.black_id.data)
        Game.create(
            white=white,
            black=black,
            winner=form.winner.data,
            handicap=form.handicap.data,
            komi=form.komi.data,
            season=form.season.data,
            episode=form.episode.data
        )
        flash('Game created!', 'success')
    else:
        flash_errors(form)
    games = Game.query.all()
    return render_template('dashboard/games.html', games=games,
                           game_create_form=form)


@blueprint.route('/games/delete/', methods=['POST'])
@login_required
def delete_game():
    """Delete a game."""
    form = GameDeleteForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        Game.delete(Game.get_by_id(form.game_id.data))
        flash('Game deleted!', 'success')
    else:
        flash_errors(form)
    return redirect(url_for('dashboard.get_games'))


@blueprint.route('/reports/', methods=['GET'])
@login_required
def get_reports():
    """Get reports page."""
    form = ReportGenerateForm(request.form, csrf_enabled=False)
    return render_template('dashboard/reports.html', report_generate_form=form)


@blueprint.route('/reports/', methods=['POST'])
@login_required
def generate_report():
    """Generate results report for submission to AGA."""
    form = ReportGenerateForm(request.form, csrf_enabled=False)
    report = None
    if form.validate_on_submit():
        report = Report(form.season.data, form.episode.data)
    else:
        flash_errors(form)
    return render_template('dashboard/reports.html', report=report,
                           report_generate_form=form)