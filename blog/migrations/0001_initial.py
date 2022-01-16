# Generated by Django 2.2 on 2022-01-16 11:19

from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='标签')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
                'db_table': 'tb_tag',
            },
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='教程名')),
            ],
            options={
                'verbose_name': '教程',
                'verbose_name_plural': '教程',
                'db_table': 'tb_tutorial',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('views', models.IntegerField(default=0, verbose_name='阅读量')),
                ('comments', models.IntegerField(default=0, verbose_name='评论量')),
                ('content', mdeditor.fields.MDTextField(verbose_name='内容')),
                ('tag', models.ManyToManyField(to='blog.Tag', verbose_name='标签')),
                ('tutorial', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Tutorial', verbose_name='教程')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'db_table': 'tb_post',
            },
        ),
    ]
