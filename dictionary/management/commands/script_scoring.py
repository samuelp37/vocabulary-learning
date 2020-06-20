from django.core.management.base import BaseCommand
import dictionary.models as models

class Command(BaseCommand):
    help = "Compute the scoring function for each word"
    def handle(self, *args, **options):
        for trs in models.Translation.objects.all():
            trs.set_heuristic()
            trs.save()
            print("###########")
            print("Translation")
            print(trs)
            print("Last date")
            print(trs.last_attempt_days)
            print("Recent succes rate")
            print(trs.last_n_success_rate)
            print("Heuristic")
            print(trs.heuristic_score)
            print("########")