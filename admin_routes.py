from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from functools import wraps
from db import get_db

admin_bp = Blueprint('admin', __name__)

def get_existing_data(table_name):
    db = get_db()
    cur = db.cursor()
    cur.execute(f'SELECT * FROM {table_name}')
    data = cur.fetchall()
    cur.close()
    return data

@admin_bp.route('/manage_teams', methods=['GET', 'POST'])
def manage_teams():
    return render_template("manage_teams.html")

@admin_bp.route('/manage_teams_add', methods=['GET', 'POST'])
def manage_teams_add():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            team_name = request.form['team_name']
            home_ground = request.form['home_ground']
            team_captain = request.form['team_captain']
            coach_id = request.form['coach_id']
            game_name= request.form['game_name']
            manager=request.form['manager']
            team_merch = request.form['team_merch']
            tournament_id=request.form['tournament_id']

            values = [team_name, home_ground, team_captain, coach_id, game_name, manager, team_merch, tournament_id]
            column_names = ["team_name", "home_ground", "team_captain", "coach_id", "game_name", "manager", "team_merch", "tournament_id"]

            if 'add' in request.form:
    
                # Parameterized query for insertion
                query = f"INSERT INTO teams ({', '.join(column_names)}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cur.execute(query, values)
                
                flash('Team added successfully', 'success')
            
        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()
        return redirect(url_for('admin.manage_teams_add'))

    cur.execute('SELECT team_id, team_name, home_ground, team_captain, coach_id, game_name, manager, team_merch, tournament_id FROM teams')
    teams = cur.fetchall()
    cur.close()
    return render_template('manage_teams_add.html', teams=teams)    


@admin_bp.route('/manage_teams_edit', methods=['GET', 'POST'])
def manage_teams_edit():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            team_id = request.form.get('team_id')
            team_name = request.form['team_name']
            home_ground = request.form['home_ground']
            team_captain = request.form['team_captain']
            coach_id = request.form['coach_id']
            game_name = request.form['game_name']
            manager = request.form['manager']
            team_merch = request.form['team_merch']
            tournament_id = request.form['tournament_id']

            # Ensure that the form is submitted with a valid team_id
            if 'edit' in request.form and team_id:
                # Prepare the update query
                query = """
                    UPDATE teams 
                    SET team_name = %s, home_ground = %s, team_captain = %s, 
                        coach_id = %s, game_name = %s, manager = %s, 
                        team_merch = %s, tournament_id = %s
                    WHERE team_id = %s
                """
                values = [team_name, home_ground, team_captain, coach_id, game_name, manager, team_merch, tournament_id, team_id]
                
                # Execute the update query
                cur.execute(query, values)
                db.commit()
                flash('Team updated successfully', 'success')

        except Exception as e:
            db.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
        finally:
            cur.close()

        return redirect(url_for('admin.manage_teams_edit'))

    # If GET request, get the team data based on team_id
    team_id = request.args.get('team_id')
    if team_id:
        cur.execute('SELECT * FROM teams WHERE team_id = %s', (team_id,))
        team = cur.fetchone()
        cur.close()

        if team:
            return render_template('manage_teams_edit.html', team=team)
        else:
            flash('Team not found', 'error')
            return redirect(url_for('admin.manage_teams_edit'))

    return render_template('manage_teams_edit.html', team=None)


@admin_bp.route('/manage_teams_delete', methods=['GET', 'POST'])
def manage_teams_delete():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            team_id = request.form.get('team_id')

            # Ensure team_id is provided and not empty
            if 'delete' in request.form and team_id:
                # Execute deletion of the team with the given team_id
                cur.execute('DELETE FROM teams WHERE team_id = %s', (team_id,))
                db.commit()
                flash('Team deleted successfully', 'success')
            else:
                flash('Please enter a valid Team ID', 'warning')

        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()
        
        # Redirect to refresh the page
        return redirect(url_for('admin.manage_teams_delete'))

    # Render the delete page (no need to fetch teams)
    return render_template('manage_teams_delete.html')

@admin_bp.route('/manage_tournaments', methods=['GET', 'POST'])
def manage_tournaments():
    return render_template("manage_tournaments.html")
  
from datetime import datetime

@admin_bp.route('/manage_tournaments_add', methods=['GET', 'POST'])
def manage_tournaments_add():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            tournament_name = request.form['tournament_name']
            start_date = request.form['start_date']  # Date format should be yyyy-mm-dd
            end_date = request.form['end_date']      # Date format should be yyyy-mm-dd

            # Print for debugging
            print(f"Form Data - Tournament Name: {tournament_name}, Start Date: {start_date}, End Date: {end_date}")

            # Prepare the query
            query = "INSERT INTO tournament (tournament_name, start_date, end_date) VALUES (%s, %s, %s)"
            values = [tournament_name, start_date, end_date]

            # Execute the query
            cur.execute(query, values)
            db.commit()

            # Check if the insertion was successful
            if cur.rowcount > 0:
                flash('Tournament added successfully', 'success')
            else:
                flash('Tournament not added, check the database constraints or data format', 'warning')

            # Print the query to check
            print(f"Executed Query: {query} with Values: {values}")

        except Exception as e:
            db.rollback()  # Rollback in case of error
            flash(f'An error occurred: {str(e)}', 'error')
            print(f"Error: {str(e)}")  # Print the error for debugging
        finally:
            cur.close()

        return redirect(url_for('admin.manage_tournaments_add'))

    return render_template('manage_tournaments_add.html')

@admin_bp.route('/manage_tournaments_edit', methods=['GET', 'POST'])
def manage_tournaments_edit():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            tournament_id = request.form['tournament_id']
            tournament_name = request.form['tournament_name']
            start_date = request.form['start_date']
            end_date = request.form['end_date']

            # Fetch the tournament by ID if it exists
            cur.execute("SELECT * FROM tournament WHERE tournament_id = %s", (tournament_id,))
            tournament = cur.fetchone()

            if tournament:
                # Update the tournament details
                cur.execute("""
                    UPDATE tournament
                    SET tournament_name = %s, start_date = %s, end_date = %s
                    WHERE tournament_id = %s
                """, (tournament_name, start_date, end_date, tournament_id))
                db.commit()

                flash('Tournament updated successfully', 'success')
            else:
                flash('Tournament not found', 'error')

        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()

        return redirect(url_for('admin.manage_tournaments_edit'))

    return render_template('manage_tournaments_edit.html')

@admin_bp.route('/manage_tournaments_delete', methods=['GET', 'POST'])
def manage_tournaments_delete():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            tournament_id = request.form['tournament_id']

            # Check if the tournament ID is provided
            if tournament_id:
                # Execute the delete query to remove the tournament by ID
                cur.execute('DELETE FROM tournament WHERE tournament_id = %s', (tournament_id,))
                db.commit()

                # If the tournament was deleted, show a success message
                if cur.rowcount > 0:
                    flash('Tournament deleted successfully!', 'success')
                else:
                    flash('Tournament ID not found.', 'warning')
            else:
                flash('Please provide a valid Tournament ID.', 'warning')

        except Exception as e:
            db.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')

        finally:
            cur.close()

        return redirect(url_for('admin.manage_tournaments_delete'))

    return render_template('manage_tournaments_delete.html')


@admin_bp.route('/manage_players', methods=['GET', 'POST'])
def manage_players():
    db = get_db()
    cur = db.cursor()

    # Fetch all players to display on the main page
    cur.execute('SELECT player_id, name, team_id, age FROM players')
    players = cur.fetchall()
    cur.close()

    return render_template('manage_players.html', players=players)


# Add Player Route
@admin_bp.route('/manage_players_add', methods=['GET', 'POST'])
def manage_players_add():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            name = request.form['name']
            team_id = request.form['team_id']
            age = request.form['age']

            # Insert the new player into the database
            query = "INSERT INTO players (name, team_id, age) VALUES (%s, %s, %s)"
            cur.execute(query, (name, team_id, age))
            db.commit()
            flash('Player added successfully', 'success')

        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()

        return redirect(url_for('admin.manage_players_add'))

    return render_template('manage_players_add.html')


# Edit Player Route
@admin_bp.route('/manage_players_edit', methods=['GET', 'POST'])
def manage_players_edit():
    db = get_db()
    cur = db.cursor()

    # If the method is POST, we're updating the player
    if request.method == 'POST':
        try:
            # Retrieve the player_id and other details from the form
            player_id = request.form['player_id']
            name = request.form['name']
            team_id = request.form['team_id']
            age = request.form['age']

            # Update the player information in the database
            query = "UPDATE players SET name = %s, team_id = %s, age = %s WHERE player_id = %s"
            cur.execute(query, (name, team_id, age, player_id))
            db.commit()
            flash('Player updated successfully', 'success')

            # After updating, redirect to the player management page or another page
            return redirect(url_for('admin.manage_players_edit'))

        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')

        finally:
            cur.close()

    # For GET request: Fetch player data based on player_id entered in the form (GET or POST)
    player_id = request.args.get('player_id')  # Try to get player_id from the URL (for initial loading)
    
    player = None  # Default to None in case no player_id is provided

    if player_id:
        try:
            # Query the database for the player with the provided player_id
            cur.execute("SELECT * FROM players WHERE player_id = %s", (player_id,))
            player = cur.fetchone()  # Fetch the player details
        except Exception as e:
            flash('Error fetching player: ' + str(e), 'error')

    cur.close()

    # If player is found, render the edit form with their data
    if player:
        return render_template('manage_players_edit.html', player=player)
    else:
        flash('Player not found', 'error')
        return render_template('manage_players_edit.html', player=None)  # Show empty form if player not found


# Delete Player Route
@admin_bp.route('/manage_players_delete', methods=['GET', 'POST'])
def manage_players_delete():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            player_id = request.form['player_id']

            # Delete the player by player_id
            if player_id:
                cur.execute('DELETE FROM players WHERE player_id = %s', (player_id,))
                db.commit()
                flash('Player deleted successfully', 'success')
            else:
                flash('Please enter a valid Player ID', 'warning')

        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()

        return redirect(url_for('admin.manage_players_delete'))

    return render_template('manage_players_delete.html')

# Main Scores Route (List all scores)
@admin_bp.route('/manage_scores', methods=['GET', 'POST'])
def manage_scores():
    db = get_db()
    cur = db.cursor()

    # Fetch all scores to display on the main page
    cur.execute('SELECT match_id, team1_score, team2_score, game_name FROM score')
    scores = cur.fetchall()
    cur.close()

    return render_template('manage_scores.html', scores=scores)

# Add Score Route
@admin_bp.route('/manage_scores_add', methods=['GET', 'POST'])
def manage_scores_add():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        try:
            team1_score = request.form['team1_score']
            team2_score = request.form['team2_score']
            game_name = request.form['game_name']

            query = "INSERT INTO score (team1_score, team2_score, game_name) VALUES (%s, %s, %s)"
            cur.execute(query, (team1_score, team2_score, game_name))
            db.commit()
            flash('Game score added successfully', 'success')

        except Exception as e:
            db.rollback()
            flash('An error occurred: ' + str(e), 'error')
        finally:
            cur.close()

        return redirect(url_for('admin.manage_scores_add'))

    return render_template('manage_scores_add.html')

# Edit Score Route
@admin_bp.route('/manage_scores_edit', methods=['GET', 'POST'])
def manage_scores_edit():
    db = get_db()
    cur = db.cursor()

    # Initialize score variable to None
    score = None

    # For GET request: Show the form with a blank or pre-filled match_id if available
    if request.method == 'GET':
        return render_template('manage_scores_edit.html', score=score)

    # For POST request: Handle the form submission to update the score
    if request.method == 'POST':
        try:
            # Retrieve form data (including match_id from the form)
            match_id = request.form.get('match_id')  # This is from the form
            team1_score = request.form.get('team1_score')
            team2_score = request.form.get('team2_score')
            game_name = request.form.get('game_name')

            # Validate that match_id is provided
            if not match_id:
                flash('Match ID is required to update the score', 'warning')
                return redirect(url_for('admin.manage_scores_edit'))  # Redirect back to the edit page if missing

            # Fetch the game score for the provided match_id from the database
            cur.execute("SELECT * FROM score WHERE match_id = %s", (match_id,))
            score = cur.fetchone()  # Fetch the score details for the match_id

            if not score:
                flash('No matching score found for the provided Match ID', 'error')
                return redirect(url_for('admin.manage_scores_edit'))  # Redirect if no record is found

            # Update the game score in the database
            query = "UPDATE score SET team1_score = %s, team2_score = %s, game_name = %s WHERE match_id = %s"
            cur.execute(query, (team1_score, team2_score, game_name, match_id))
            db.commit()

            flash('Game score updated successfully', 'success')
            return redirect(url_for('admin.manage_scores_edit'))  # Redirect to the scores list after update
        except Exception as e:
            db.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('admin.manage_scores_edit'))  # Redirect to the edit page if error occurs
        finally:
            cur.close()

    # If for some reason, no match_id was found in POST data, return to edit page
    flash('Match ID not found in form', 'error')
    return redirect(url_for('admin.manage_scores_edit'))

@admin_bp.route('/manage_scores_delete', methods=['GET', 'POST'])
def manage_scores_delete():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        # Retrieve the match_id from the form
        match_id = request.form.get('match_id')

        if match_id:
            try:
                # Delete the game score from the database based on the match_id
                cur.execute("DELETE FROM score WHERE match_id = %s", (match_id,))
                db.commit()

                flash('Game score deleted successfully', 'success')
            except Exception as e:
                db.rollback()
                flash(f'An error occurred: {str(e)}', 'error')

        else:
            flash('Match ID is required to delete a game score', 'warning')

    # Render the delete form template
    return render_template('manage_scores_delete.html')
