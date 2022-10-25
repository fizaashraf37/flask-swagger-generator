import os
import pathlib

from deepdiff import DeepDiff
from flask import Blueprint, jsonify
from flask_testing import TestCase

from flask_swagger_generator.generators import Generator
from flask_swagger_generator.components import SwaggerVersion
from tests.resources.app_base import create_app
from tests.resources.utils import yaml_as_dict

app = create_app()
generator = Generator.of(SwaggerVersion.VERSION_THREE)
blueprint = Blueprint('objects', __name__)


@blueprint.route('/path-path/<path:path>')
def get_path_url(name):
    return jsonify({'id': 1, 'name': 'test_object_name'}), 200


@blueprint.route('/int-path/<int:int>')
def get_int_url(name):
    return jsonify({'id': 1, 'name': 'test_object_name'}), 200


@blueprint.route('/string-path/<string:string>')
def get_string_url(name):
    return jsonify({'id': 1, 'name': 'test_object_name'}), 200


@blueprint.route('/float-path/<float:float>')
def get_num_url(name):
    return jsonify({'id': 1, 'name': 'test_object_name'}), 200


app.register_blueprint(blueprint)


class AppTestBase(TestCase):

    def setUp(self) -> None:
        super(AppTestBase, self).setUp()

    def create_app(self):
        return app

    def tearDown(self):
        super(AppTestBase, self).tearDown()

    def test(self):
        generated_swagger_path = os.path.join(
            pathlib.Path(__file__).parent.parent.absolute()
        ) + '/resources/generated.yaml'
        correct_swagger_path = os.path.join(
            pathlib.Path(__file__).parent.parent.absolute()
        ) + '/resources/swagger_version_three/url_path_parameter_swagger.yaml'
        generator.generate_swagger(self.app, generated_swagger_path)
        generated_yaml = yaml_as_dict(generated_swagger_path)
        reference_yaml = yaml_as_dict(correct_swagger_path)
        reference_yaml['info'].pop('description')
        generated_yaml['info'].pop('description')
        difference = DeepDiff(generated_yaml, reference_yaml, ignore_order=True)
        self.assertEqual({}, difference)
