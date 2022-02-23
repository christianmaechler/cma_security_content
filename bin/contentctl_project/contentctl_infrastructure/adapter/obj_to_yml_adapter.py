import os
import re

from contentctl_infrastructure.adapter.yml_writer import YmlWriter
from contentctl_core.application.adapter.adapter import Adapter
from contentctl_core.domain.entities.enums.enums import SecurityContentType


class ObjToYmlAdapter(Adapter):

    def writeObjectsInPlace(self, objects: list) -> None:
        for object in objects:
            file_path = object['file_path']
            object.pop('file_path')
            object.pop('deprecated')
            object.pop('experimental') 
            YmlWriter.writeYmlFile(file_path, object)


    def writeObjects(self, objects: list, output_path: str, type: SecurityContentType = None) -> None:
        for obj in objects:
            file_name = "ssa___" + self.convertNameToFileName(obj)
            if self.isComplexBARule(obj.search):
                file_path = os.path.join(output_path, 'complex', file_name)
            else:
                file_path = os.path.join(output_path, 'srs', file_name)

            # remove unncessary fields
            YmlWriter.writeYmlFile(file_path, obj.dict(
                include =
                    {
                        "name": True,
                        "id": True,
                        "version": True,
                        "description": True,
                        "search": True,
                        "how_to_implement": True,
                        "known_false_positives": True,
                        "references": True,
                        "tags": 
                            {
                                "analytic_story": True,
                                "cis20" : True,
                                "nist": True,
                                "kill_chain_phases": True,
                                "mitre_attack_id": True,
                                "risk_severity": True,
                                "security_domain": True,
                                "required_fields": True
                            },
                        "test": 
                            {
                                "name": True,
                                "tests": {
                                    '__all__': 
                                        {
                                            "name": True,
                                            "file": True,
                                            "pass_condition": True,
                                            "attack_data": {
                                                '__all__': 
                                                {
                                                    "file_name": True,
                                                    "data": True,
                                                    "source": True
                                                }
                                            }
                                        }
                                }
                            }
                    }
                ))


    def convertNameToFileName(self, obj: dict):
        file_name = obj.name \
            .replace(' ', '_') \
            .replace('-','_') \
            .replace('.','_') \
            .replace('/','_') \
            .lower()
        file_name = file_name + '.yml'
        return file_name


    def isComplexBARule(self, search):
        return re.findall("stats|first_time_event|adaptive_threshold", search)

