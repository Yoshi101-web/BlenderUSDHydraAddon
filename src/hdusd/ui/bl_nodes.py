#**********************************************************************
# Copyright 2020 Advanced Micro Devices, Inc
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#********************************************************************
import MaterialX as mx

import bpy
from bpy_extras.io_utils import ExportHelper

from . import HdUSD_Panel, HdUSD_Operator

from ..utils import logging
log = logging.Log(tag='ui.mx_nodes')


class HDUSD_MATERIAL_OP_export_mx_file(HdUSD_Operator, ExportHelper):
    bl_idname = "hdusd.material_export_mx_file"
    bl_label = "MaterialX Export to File"
    bl_description = "Export material as MaterialX node tree to .mtlx file"

    filename_ext = ".mtlx"
    filepath: bpy.props.StringProperty(
        name="File Path",
        description="File path used for exporting material as MaterialX node tree to .mtlx file",
        maxlen=1024, subtype="FILE_PATH"
    )
    filter_glob: bpy.props.StringProperty(default="*.mtlx", options={'HIDDEN'}, )

    def execute(self, context):
        doc = context.material.hdusd.export()
        if not doc:
            return {'CANCELLED'}

        mx.writeToXmlFile(doc, self.filepath)
        return {'FINISHED'}


class HDUSD_MATERIAL_OP_export_mx_console(HdUSD_Operator):
    bl_idname = "hdusd.material_export_mx_console"
    bl_label = "MaterialX Export to Console"
    bl_description = "Export material as MaterialX node tree to console"

    def execute(self, context):
        doc = context.material.hdusd.export()
        if not doc:
            return {'CANCELLED'}

        print(mx.writeToXmlString(doc))
        return {'FINISHED'}


class HDUSD_MATERIAL_PT_import_export(HdUSD_Panel):
    bl_label = "Import/Export"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Tool"

    @classmethod
    def poll(cls, context):
        tree = context.space_data.edit_tree
        return super().poll(context) and tree and \
               tree.bl_idname == bpy.types.ShaderNodeTree.__name__

    def draw(self, context):
        layout = self.layout

        layout.operator(HDUSD_MATERIAL_OP_export_mx_file.bl_idname)
        layout.operator(HDUSD_MATERIAL_OP_export_mx_console.bl_idname)
