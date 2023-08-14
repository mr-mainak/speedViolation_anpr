import yaml

surv_area = [
        {
            'speed_region' : {
                'region_1' : [(0,126),(799,136),(799,397),(0,380)],
                'region_2' : [(0,380),(799,397),(799,526),(0,526)]
            },


            "trigger_line" : {
                "line" : [(0,460),(799,460)]
            }
        }
    ]

with open('laneConfig.yaml', 'w') as yamlfile:
    data = yaml.dump(surv_area, yamlfile)
    print("write successful")
