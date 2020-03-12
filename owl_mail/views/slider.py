import random

class Slider():

    def random_picture(self):
        pictures = [
            'https://i.pinimg.com/originals/5c/38/7b/5c387b8908206935ae0af08822cb9b61.jpg',
            'https://wallpapermemory.com/uploads/722/harry-potter-and-the-deathly-hallows-part-2-wallpaper-1080p-32526.jpg',
            'https://4kwallpaper.org/wp-content/uploads/Harry-Potter-Logo-Wallpapers010.jpg',
            'https://i.pinimg.com/originals/c6/fc/d8/c6fcd8ca16c4d943b1f284333cfd0efc.jpg',
            'https://monodomo.com/free-wallpapers/harry-potter-background-For-Free-Wallpaper.jpg',
            'https://wallpapercave.com/wp/wp1850856.jpg'
        ]
        picture = random.choice(pictures)
        return picture