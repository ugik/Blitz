from django.core.management.base import BaseCommand
from django.conf import settings

from base.models import Heading

class Command(BaseCommand):

    def handle(self, *args, **options):

#        import pdb; pdb.set_trace()

# setup headings
        head = Heading.objects.create(location = "*",
                  saying = "I have never met a successful excuse maker.",
                  author = "Nav-Vii")
        head = Heading.objects.create(location = "*",
                  saying = "I only start counting when it starts hurting because they're the only ones that count.",
                  author = "Muhammed Ali")
        head = Heading.objects.create(location = "*",
                  saying = "Its hard to beat a person who never gives up.",
                  author = "Babe Ruth")
        head = Heading.objects.create(location = "*",
                  saying = "Strength does not come from physical capacity. It comes from an indomitable will. ",
                  author = "Gandhi")
        head = Heading.objects.create(location = "*",
                  saying = "I've failed over and over and over again in my life. And that is why I succeed. ",
                  author = "Michael Jordan")
        head = Heading.objects.create(location = "*",
                  saying = "No one ever drowned in sweat.",
                  author = "Lou Holtz")
        head = Heading.objects.create(location = "*",
                  saying = "Strong is what happens when you run out of weak.",
                  author = "Nicole Nichols")
        head = Heading.objects.create(location = "*",
                  saying = "A one-hour workout is 4% of your day. No excuses.",
                  author = "Geoff Bagshaw")
        head = Heading.objects.create(location = "*",
                  saying = "Forget the 'no' in your head and listen to the 'yes' in your body.",
                  author = "Paul Katami")
        head = Heading.objects.create(location = "*",
                  saying = "When you think about quitting, think about why you started.",
                  author = "Anonymous")
        head = Heading.objects.create(location = "*",
                  saying = "I saw a woman wearing a sweatshirt with 'Guess' on it. I said, 'Thyroid problem?'",
                  author = "Arnold Schwarzenegger")
        head = Heading.objects.create(location = "*",
                  saying = "Our growing softness, our increasing lack of physical fitness, is a menace to our security.",
                  author = "John F. Kennedy")
        head = Heading.objects.create(location = "*",
                  saying = "Pain makes me grow. Growing is what I want. Therefore, for me pain is pleasure.",
                  author = "Arnold Schwarzenegger")
        head = Heading.objects.create(location = "*",
                  saying = "Sweat is weakness leaving the body.",
                  author = "Anonymous")
        head = Heading.objects.create(location = "*",
                  saying = "Real g's move in silence like lasagna.",
                  author = "Lil Wayne")
        head = Heading.objects.create(location = "*",
                  saying = "I don't know, man. I guess I'm gonna fade into Bolivian.",
                  author = "Mike Tyson")
        head = Heading.objects.create(location = "*",
                  saying = "My image is a strategic hot mess.",
                  author = "Miley Cyrus")
        head = Heading.objects.create(location = "*",
                  saying = "I'm addicted to perfection.",
                  author = "Mike Tyson")
        head = Heading.objects.create(location = "*",
                  saying = "These dudes are trying to crucify me and I'm like 'Bro, do you even lift?'",
                  author = "Jesus of Nazareth")
        head = Heading.objects.create(location = "*",
                  saying = "Hoes on my dick cuz I look like Jesus.",
                  author = "Lil B")
        head = Heading.objects.create(location = "*",
                  saying = "I don't workout my legs cause then I can't fit into skinny jeans, I don't workout my back cause I can't see it.",
                  author = "Dom Mazzetti")
        head = Heading.objects.create(location = "*",
                  saying = "If a brick didn't know how to sit on walls no mo' ... What would you ask it?",
                  author = "The ODB")
        head = Heading.objects.create(location = "*",
                  saying = "Greatness is what we on the brink of",
                  author = "Nicki Minaj")


