import json
import pygame


class Mission:
    def __init__(self):
        self.filename = 'missions.json'
        self.missions = self.load_missions()
        self.current_mission = self._get_next_incomplete_mission()

    def _get_next_incomplete_mission(self):
        for mission in self.missions:
            if not mission["is_completed"]:
                return mission
        print("All missions are complete!")
        return None
    def load_missions(self):
        with open(self.filename, "r",encoding="utf-8") as f:
            missions = json.load(f)
        return missions

    def update_mission_progress(self, mission_id):
        for mission in self.missions:
            if mission["id"] == mission_id:
                mission["progress"] += 1
                if mission["progress"] >= mission["goal"]:
                    mission["is_completed"] = True
                    print(f"Mission '{mission['title']}' completed!")
                    self.current_mission += 1
                break
        else:
            print("Mission not found.")
    def next_mission(self):
        for mission in self.missions:
            if mission["id"] == self.current_mission["id"]:
                mission["is_completed"] = True
                self.current_mission = self._get_next_incomplete_mission()
                break
        else:
            print("Mission not found.")
    def draw_mission(self,screen):
        pass
    def save_missions(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.missions, f, indent=4, ensure_ascii=False)
        #with open(self.filename, "w") as f:
        #    json.dump(self.missions, f, indent=4)
    def get_not_completed_missions(self):
        return [mission for mission in self.missions if not mission["is_completed"]]
    def get_completed_missions(self):
        return [mission for mission in self.missions if mission["is_completed"]]
    def get_current_mission(self):
        return self.current_mission
    def get_mission_id(self):
        return self.current_mission["id"]


    def update_dialog_start(self):
        for mission in self.missions:
            if mission["id"] == self.current_mission["id"]:
                mission["dialog_start"] = True
                break
        else:
            print("Mission not found.")
    def update_dialog_end(self):
        for mission in self.missions:
            if mission["id"] == self.current_mission["id"]:
                mission["dialog_end"] = True
                break
        else:
            print("Mission not found.")