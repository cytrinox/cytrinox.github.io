---
layout: post
title: "First Light: Balkonsternwarte"
banner_image: theme_astro2.jpg
tags: [astronomy, photography]
category: imaging
---

Ein Balkon mit Südblick ist eine tolle Gelegenheit für astronomische Beobachtungen. Wenn dann auch noch
die Sicht nach Norden und auf den Polarstern frei sind, gehört auf den Balkon selbstverständlich ein Teleskop
zur Himmelsbeobachtung.

Den Traum einer kleinen Balkonsternwarte habe ich mir nun erfüllt. Da größere Optiken und Brennweiten mitten
im Stadtgebiet eher nicht in Frage kommen und ich mit den Skywatcher Montierungen ganz gute Erfahrungen gemacht
habe, fiel die Wahl auf die Skywatcher HEQ-5. Zusammen mit einem Leitrohr und M-GEN Autoguider, einer bereits
vorhandene Canon 40Da und einigen EF Objektive sowie einem Haufen Zubehör, waren im Dezember '17 endlich alle
notwenigen Teile beschafft.


<!--more-->


# Montierung und Optiken

Die HEQ-5 Montierung wurde von VTSB optimiert. Ich bin mir nicht hunderprozentig sicher, ob sich das lohnt,
aber die Kommentare und Erfahrungberichte in diversen Astro-Foren waren ganz gut und da die HEQ-5 schließlich
nur für Astrofotografie verwendet werden sollte, hielt ich es für eine sinnvolle Investition.

Die Traglast der Montierung ist nun nicht sonderlich hoch, aber für Leitrohr, Canon DSLR und Objektiv reicht
es allemal aus, selbt ein APO wäre noch problemlos möglich und ein geringes Gewicht des ganzen Aufbaus hat
ja auch wieder Vorteile, speziell wenn man alles ganz schnell mal auf den Balkon stellen möchte.

{% include image_mini_caption.html imageurl="/images/posts/sternwarte_aufbau.jpg" caption="HEQ-5 Montierung" %}

Als Aufnahmekamera kommt eine Canon 40D zum Einsatz, die vor Jahren schon astromodifiziert wurde und die ich immer
mal wieder für kurzbelichtete Aufnahmen auf einer Skywatcher StarAdventurer Montierung verwendet habe.


Mit EF Bennweiten von 85mm und 100mm im Schrank war die Frage nach den Optiken sehr schnell gelöst.
Ein APO wäre natürlich super, aber da ich gerade Widefield Aufnahmen sehr faszinierend finde und
sich hierzu Brennweiten von 100-200mm sehr gut eignen, werde ich erstmal mit dem arbeiten, was bereits
an Linsen vorhanden ist. 

# Steuerung und Elektronik

Der knifflige Part war die Planung der Stromversorung, Steuerung und Kalibierung der Montierung,
sowie schlussendlich die Aufnahmesteuerung.

Glücklicherweise liegt mein Arbeitszimmer direkt neben dem Balkon und das Kabel einer nicht mehr
genutzten Satellitenschlüssel hinterließ ein offenes Loch in der Wand nach draußen.

Der Plan war also, ein USB Kabel vom Computer auf den Balkon zu legen und dort in einer wetterfesten
USB-Buchse enden zu lassen. Mit einem Spezialkabel geht es dann von der Buchse weiter bis zu einem
USB-Hub, der mit Klettband am Stativbein der Montierung befestigt ist und über einen mobilen
Bleigelakku eine zusätzliche, separate Stromversorgung erhält.

{% include image_mini_caption.html imageurl="/images/posts/sternwarte_usb1.jpg" caption="Wetterfestes USB Kabel" %}

Der Bleigelakku versorgt ebenso den M-GEN, die HEQ-5 Montierung und ggf. anderes kleines Zubehör.
Die DSLR Kamera und die Heizbänder werden an der regulären 220V Stromversorgung angeschlossen.

Der Hintergedanke bei der Planung war, dass das komplette Setup auch für einen Einsatz auf dem Acker
geeignet ist. Die Heizbänder können ggf. auch via USB direkt am Beigelakku angschlossen werden
und die Kamera lässt sich auch mit Akkus oder zusätzlichem KFZ Adapter betreiben.

Alle elektronischen Geräte, die per USB gesteuert werden können, hängen am USB Hub und über die Leitung
ins Arbeitszimmer erfolgt die Steuerung vom Computer aus.

{% include image_mini_caption.html imageurl="/images/posts/sternwarte_usb2.jpg" caption="Wetterfestes USB Kabel" %}

## EQMod: Steuerung der HEQ-5 Montierung

Mit dem ASCOM Framework und der EQMod Software kann die HEQ-5 via USB gesteuert und kalibiert werden.
Also auch das Star Alignment und Polar Alignment kann damit erfolgen.
Über die Einrichtung der EQMod Software gibt es schon viele Artikel, daher klammere ich das an dieser Stelle
aus, ingesamt war das Setup aber ohne nennenswerte Probleme machbar. Die Kopplung an Stellarium
ermöglicht die direkte Steuerung der Montierung, d.h. die Auswahl eines beliebigen Objektes das
die Montierung anschließend anfährt.

{% include image_mini_caption.html imageurl="/images/posts/sternwarte_eqmod.jpg" caption="EQMOD Software" %}

## APT: Steuerung der DSLR Kamera

APT ist eine sehr praktische und zuverlässige Software für die Planung und Steuerung von
Aufnahmen. Über ASCOM ist eine Verbindung zwischen APT und EQMod möglich. APT kann ebenfalls
den M-GEN über USB steuern. Dadurch können Funktionen wie Dithering zwischen zwei Aufnahmen vom M-GEN
durchgeführt werden, obwohl die Aufnahmesteuerung von APT übernommen wird und nicht wie sonst üblich vom M-GEN.

{% include image_mini_caption.html imageurl="/images/posts/sternwarte_apt.jpg" caption="APT Software" %}

Die Korrektursignale des M-GEN gehen bei diesem Setup nach wie vor direkt über das ST-4 Kabel an die Montierung.
APT informiert über die USB-Verbindung den M-GEN aber darüber, wenn eine Aufnahme läuft bzw. abgeschlossen ist
und kann dadurch dem M-GEN die Zeitspanne einräumen, die für die Neupositionierung zwecks Dithering notwendig ist.

Über Plate-Solving kann APT sogar die Einordnung der Montierung erhöhen. Dazu gibt man in APT
die Koordinaten der gewünschten Position ein und lässt die Montierung diesen Punkt anfahren. Anschließend
erstellt APT mehrere Aufnahmen, ermittelt jeweils über Plate-Solving die tatsächlichen Koordinaten, errechnet die Korrektur,
übergibt diese an EQMod und fährt die korrigierte Position an. Dieser Schritt wird dann so oft wiederholt,
bis die Position perfekt ist.

Diesen Mechanismus korrekt einzurichten und zu verstehen ist am Anfang gar nicht so leicht, aber mit dem Handbuch
und einigen Experimenten klappt dies sehr zuverlässig.

Über die Aufnahmepläne in APT ist es dann möglich, zeitgesteuert z.B. 20x 5min zu belichten und die RAW Datei
automatisch auf den Rechner zu übertragen - der Hauptzweck der Software.


# Zubehör

Da die Linsen der Optiken oft schnell beschlagen, habe ich sowohl dem Leitrohr als auch dem EF Objektiv
ein USB-Heizband spendiert. Die ziehen recht viel Strom und sollten daher nicht am Bleigelakku hängen (was
bei einem Einsatz auf dem Acker aber für 4-6 Stunden möglich ist). Daher kommt hier noch ein zusätzlicher
USB-Hub von Anker mit extra dicker Stromversorung zum Einsatz.


# Schmalbandfilter

Da ich aus dem Stadtgebiet heraus fotografiere, stand für mich von Anfang an fest, dass ich mit Schmalbandfiltern
arbeiten muss. Einen Astronomik Ha 6nm EOS Clipfilter hatte ich bereits, der bei Tests auch schon sehr viel
bessere Kontraste zeigte. Ein OIII 6nm Filter wird nach dem First-Light noch dazukommen, dann sind zumindest Bicolor-Fotos
möglich. Wenn alles gut läuft, vielleicht auch ein SII Filter für Fotos in der Hubble-Palette.

{% include image_mini_caption.html imageurl="/images/posts/sternwarte_clipfilter.jpg" caption="Clipfilter in Canon 40D" %}

Die Clipfilter sind eigentlich eine praktische Erfindung, denn sie ermöglichen Schmalbandfotorgafie mit einer DSLR Kamera.
In der Nachbearbeitung ist es jedoch etwas trickreich, denn die Bayer-Matrix der DSLR Sensoren ist nicht so recht kompatibel
mit Schmalbandfiltern. Bei einem Ha Filter beispielsweise werden ja nur die R-Pixel der RGGB Bayer-Matrix belichtet.
Die GGB Pixel enthalten dann nur Rauschen. Wird in der Bildbearbeitung dann ein Debayer-Algorithmus wie z.B. VNG angewendet,
rechnet dieser auch das nutzlose Rauschen mit ein.

Als besserer Workflow scheint mir (nach bisherigen Tests), wenn als Debayer-Algorithmus **Superpixel** gewählt wird.
Dadurch wird das Bild zwar kleiner, aber die Farbwerte werden nicht miteinander verrechnet, sondern einfach nur
in ein Farbpixel mit den RGB-Werten überführt. Danach kann man den gewünschten Farbkanal, bei Ha also den R Kanal,
extrahieren und hat als Ergebnis ein sauberes Graustufenbild.

{% include image_mini_caption.html imageurl="/images/posts/sternwarte_noise_G.jpg" caption="Grün-Kanal bei Ha-Filter enthält nur Rauschen" %}

Bei Flatfield-Aufnahmen sollte der Filter übrigens eingesetzt bleiben, denn dieser kann ja auch Staub und Kratzer
enthalten und den optischen Weg verändern. Mit einer Flatfieldfolie beträgt die Belichtungszeit pro Flat
und 6nm Filter ca. 1-2 Sekunden. Hier muss man einfach viel experimentieren und die Histogramme der Flats
prüfen, bis man den optimalen Wert gefunden hat.

## Fokusieren mit Clipfilter
Das war tatsächlich das größte Problem. Für das Alignment der Montierung
benötigt man einen hellen Stern, der via Liveview auch in APT zu erkennen ist. Fokusiert man jedoch auf einen Stern
und setzt dann den Filter ein, ändert sich der optische Weg und der Fokus sitzt falsch. 
Auch der Filterwechsel während einer Aufnahme ist problematisch. Ich habe zwar eine Schelle verwendet, um das Objektiv
auf der Montierung zu befestigen, d.h. ich muss nur die Kamera vom Objektiv lösen und nicht umgekehrt, trotzdem
muss man aufpassen dass sich dabei der Fokus nicht verändert.
Zwar werden die Clipfilter als **homofokal** beworben, d.h. die optische Dicke ist identisch und der Fokuspunkt bleibt
gleich, trotzdem gibt es winzige Toleranzen und wer hier Perfektion haben möchte, muss trotzdem nachfokusieren.

Es gibt aber zwei Hilfsmittel: ein Klarglasfilter, der schon während des Star Alignment eingebaut werden kann.
Dadurch stimmt der Fokus schonmal sehr gut. Wenn dann ein richtiger Filter eingesetzt wird, sind die Abweichungen
minimal. Und ein Schraubfilter für das Objektiv, eine sog. Bahtinov-Maske. Diese Maske ermöglicht ein absolut
exaktes Fokusieren. Da dieser nur ganz leicht auf das Objektiv aufgeschraubt sein muss läuft man auch nicht Gefahr,
den Fokus ungewollt zu verändern, wenn das Hilfsmittel wieder entfernt wird.

{% include image_mini_caption.html imageurl="/images/posts/sternwarte_bahtinov.jpg" caption="Bahtinov Maske als Schraubfilter" %}

Die Bahtinov-Maske erzeugt durch das Muster drei Linien, die sich bei exaktem Fokus alle in einem gemeinsamen
Punkt kreuzen.

{% include image_mini_caption.html imageurl="/images/posts/sternwarte_focus.gif" caption="Simulation einer Bahtinov-Maske, CC-SA Niels Noordhoek" %}

# First-Light

Als erstes Objektiv habe ich (natürlich) das Sternbild Orion gewählt, dessen Gürtel und Umgebung
sehr tolle Ha-Nebel zeigt.


{% include image_caption.html imageurl="/images/posts/sternwarte_orion.jpg" caption="Orion Gürtel mit Ha-Filter" %}
