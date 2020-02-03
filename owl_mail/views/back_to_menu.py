from flask import redirect, url_for

class Menu():
    
    def back(self, endpoint):
        self.menu = endpoint
        return redirect(url_for(self.menu))
