from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    birth_date = models.DateField(null=True, blank=True)

    CITY_CHOICES = [
        ("Agadir", "Agadir"),
        ("Al Hoceïma", "Al Hoceïma"),
        ("Azilal", "Azilal"),
        ("Ben Guerir", "Ben Guerir"),
        ("Beni Mellal", "Beni Mellal"),
        ("Benslimane", "Benslimane"),
        ("Berrechid", "Berrechid"),
        ("Berkane", "Berkane"),
        ("Biougra", "Biougra"),
        ("Boujdour", "Boujdour"),
        ("Boulemane", "Boulemane"),
        ("Casablanca", "Casablanca"),
        ("Chefchaouen", "Chefchaouen"),
        ("Chichaoua", "Chichaoua"),
        ("Dakhla", "Dakhla"),
        ("El Jadida", "El Jadida"),
        ("El Kelaâ des Sraghna", "El Kelaâ des Sraghna"),
        ("Errachidia", "Errachidia"),
        ("Essaouira", "Essaouira"),
        ("Fes", "Fes"),
        ("Figuig", "Figuig"),
        ("Fkih Ben Saleh", "Fkih Ben Saleh"),
        ("Fnideq", "Fnideq"),
        ("Guelmim", "Guelmim"),
        ("Inzegan", "Inzegan"),
        ("Kenitra", "Kenitra"),
        ("Khemisset", "Khemisset"),
        ("Khenifra", "Khenifra"),
        ("Khouribga", "Khouribga"),
        ("Ksar El Kbir", "Ksar El Kbir"),
        ("Larache", "Larache"),
        ("Laayoune", "Laayoune"),
        ("Marrakech", "Marrakech"),
        ("Meknes", "Meknes"),
        ("Mohammedia", "Mohammedia"),
        ("Nador", "Nador"),
        ("Ouarzazate", "Ouarzazate"),
        ("Oujda", "Oujda"),
        ("Ouazzane", "Ouazzane"),
        ("Oulad Teima", "Oulad Teima"),
        ("Rabat", "Rabat"),
        ("Safi", "Safi"),
        ("Sale", "Sale"),
        ("Sefrou", "Sefrou"),
        ("Settat", "Settat"),
        ("Sidi Ifni", "Sidi Ifni"),
        ("Sidi Kacem", "Sidi Kacem"),
        ("Sidi Slimane", "Sidi Slimane"),
        ("Es-Semara", "Es-Semara"),
        ("Taounate", "Taounate"),
        ("Tan-Tan", "Tan-Tan"),
        ("Taroudant", "Taroudant"),
        ("Tata", "Tata"),
        ("Taza", "Taza"),
        ("Tiznit", "Tiznit"),
        ("Tangier", "Tangier"),
        ("Temara", "Temara"),
        ("Tetouan", "Tetouan"),
        ("Taourirt", "Taourirt"),
        ("Wad Zam", "Wad Zam"),
        ("Youssoufia", "Youssoufia"),
    ]

    city = models.CharField(max_length=100, choices=CITY_CHOICES)

    def __str__(self):
        return self.email
