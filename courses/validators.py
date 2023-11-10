from rest_framework import serializers


def validator_links(url):
    if not url.startswith('http://www.youtube.com/'):
        raise serializers.ValidationError('Invalid link!')
