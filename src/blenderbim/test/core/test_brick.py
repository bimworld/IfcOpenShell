# BlenderBIM Add-on - OpenBIM Blender Add-on
# Copyright (C) 2021 Dion Moult <dion@thinkmoult.com>
#
# This file is part of BlenderBIM Add-on.
#
# BlenderBIM Add-on is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BlenderBIM Add-on is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BlenderBIM Add-on.  If not, see <http://www.gnu.org/licenses/>.

import blenderbim.core.brick as subject
from test.core.bootstrap import ifc, brick


class TestLoadBrickProject:
    def test_run(self, brick):
        brick.load_brick_file("filepath").should_be_called()
        brick.import_brick_classes("Class").should_be_called()
        brick.set_active_brick_class("Class").should_be_called()
        subject.load_brick_project(brick, filepath="filepath")


class TestViewBrickClass:
    def test_run(self, brick):
        brick.add_brick_breadcrumb().should_be_called()
        brick.clear_brick_browser().should_be_called()
        brick.import_brick_classes("brick_class").should_be_called()
        brick.import_brick_items("brick_class").should_be_called()
        brick.set_active_brick_class("brick_class").should_be_called()
        subject.view_brick_class(brick, brick_class="brick_class")


class TestViewBrickItem:
    def test_run(self, brick):
        brick.add_brick_breadcrumb().should_be_called()
        brick.clear_brick_browser().should_be_called()
        brick.get_item_class("item").should_be_called().will_return("brick_class")
        brick.import_brick_classes("brick_class").should_be_called()
        brick.import_brick_items("brick_class").should_be_called()
        brick.set_active_brick_class("brick_class").should_be_called()
        brick.select_browser_item("item").should_be_called()
        subject.view_brick_item(brick, item="item")


class TestRewindBrickClass:
    def test_run(self, brick):
        brick.pop_brick_breadcrumb().should_be_called().will_return("previous_class")
        brick.clear_brick_browser().should_be_called()
        brick.import_brick_classes("previous_class").should_be_called()
        brick.import_brick_items("previous_class").should_be_called()
        brick.set_active_brick_class("previous_class").should_be_called()
        subject.rewind_brick_class(brick)


class TestCloseBrickProject:
    def test_run(self, brick):
        brick.clear_project().should_be_called()
        subject.close_brick_project(brick)


class TestConvertBrickProject:
    def test_run(self, ifc, brick):
        brick.get_brick_path_name().should_be_called().will_return("foo.ttl")
        ifc.run("library.add_library", name="foo.ttl").should_be_called().will_return("library")
        brick.get_brick_path().should_be_called().will_return("/path/to/foo.ttl")
        ifc.run(
            "library.edit_library", library="library", attributes={"Location": "/path/to/foo.ttl"}
        ).should_be_called()
        subject.convert_brick_project(ifc, brick)


class TestAssignBrickReference:
    def test_assigning_to_a_new_reference(self, ifc, brick):
        brick.get_library_brick_reference("library", "brick").should_be_called().will_return(None)
        ifc.run("library.add_reference", library="library").should_be_called().will_return("reference")
        brick.export_brick_attributes("brick").should_be_called().will_return("attributes")
        ifc.run("library.edit_reference", reference="reference", attributes="attributes").should_be_called()
        ifc.get_entity("obj").should_be_called().will_return("product")
        ifc.run("library.assign_reference", product="product", reference="reference").should_be_called()
        subject.assign_brick_reference(ifc, brick, obj="obj", library="library", brick_uri="brick")

    def test_assigning_to_an_existing_reference(self, ifc, brick):
        brick.get_library_brick_reference("library", "brick").should_be_called().will_return("reference")
        ifc.get_entity("obj").should_be_called().will_return("product")
        ifc.run("library.assign_reference", product="product", reference="reference").should_be_called()
        subject.assign_brick_reference(ifc, brick, obj="obj", library="library", brick_uri="brick")
