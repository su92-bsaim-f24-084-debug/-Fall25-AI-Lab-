class ModelBasedReflexAgent:
    def __init__(self, desired_temperature):
        self.desired_temperature = desired_temperature
        with open("mem.txt","a") as file:
            pass
    def perceive(self, current_temperature):
        return current_temperature
    def check_history(self,temp):
        with open("mem.txt","r") as file:
            l= file.readlines()
            for i in l:
                t , a = i.strip().split(",")
                print()
                if int(t) == temp:
                    return a
        return None
    def act(self, current_temperature):
        action = self.check_history(current_temperature)
        if action:
            print("From history")
        elif current_temperature <= self.desired_temperature:
            action = "Turn off AC"
            with open("mem.txt","a") as file:
                file.write(f"{current_temperature},{action}\n")
        elif current_temperature>self.desired_temperature:
            action = "Turn on AC"
            with open("mem.txt","a") as file:
                file.write(f"{current_temperature},{action}\n")
        return action
# simulating different rooms with different current temperatures
rooms = {
"Living Room": 18,
"Bedroom": 32,
"Kitchen": 30,
"Bathroom": 24,
"Master_Bedroom":27
}
# desired temperature for all rooms
desired_temperature = 20
agent = ModelBasedReflexAgent(desired_temperature)
# run the agent for each room
for room, temperature in rooms.items():
    action = agent.act(temperature)
    print(f"{room}: Current temperature = {temperature}°C. {action}.")
