import pytest
from sqlalchemy.exc import IntegrityError

from app import app
from models import db, Recipe, User

class TestRecipe:
    '''User in models.py'''

    def test_has_attributes(self):
        '''has attributes title, instructions, and minutes_to_complete.'''
    
        with app.app_context():
            # First create a test user
            user = User(
                username="testuser",
                image_url="test.jpg",
                bio="test bio"
            )
            user.password_hash = "password"  # Use the proper setter method
            db.session.add(user)
            db.session.commit()

            Recipe.query.delete()
            db.session.commit()
    
            recipe = Recipe(
                title="Delicious Shed Ham",
                instructions="""Or kind rest bred with am shed then. In""" + \
                    """ raptures building an bringing be. Elderly is detract""" + \
                    """ tedious assured private so to visited. Do travelling""" + \
                    """ companions contrasted it. Mistress strongly remember""" + \
                    """ up to. Ham him compass you proceed calling detract.""" + \
                    """ Better of always missed we person mr. September""" + \
                    """ smallness northward situation few her certainty""" + \
                    """ something.""",
                minutes_to_complete=60,
                user_id=user.id
            )
    
            db.session.add(recipe)
            db.session.commit()

            new_recipe = Recipe.query.filter(Recipe.title == "Delicious Shed Ham").first()
            assert new_recipe.title == "Delicious Shed Ham"
            assert new_recipe.instructions.startswith("Or kind rest bred with am shed then")
            assert new_recipe.minutes_to_complete == 60

    def test_requires_title(self):
        '''requires each record to have a title.'''
        
        with app.app_context():
            with pytest.raises(ValueError):
                recipe = Recipe(instructions="test", minutes_to_complete=60)
                db.session.add(recipe)
                db.session.commit()

    def test_requires_50_plus_char_instructions(self):
        '''requires instructions to be at least 50 characters long.'''
        
        with app.app_context():
            with pytest.raises(ValueError):
                recipe = Recipe(
                    title="Generic Ham",
                    instructions="idk lol")
                db.session.add(recipe)
                db.session.commit()
                