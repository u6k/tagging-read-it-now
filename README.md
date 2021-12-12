# Tagging Read-it-now _(tagging-read-it-now)_

> すぐ読みたい記事にタグ付けする

## Install

Dockerを使用します。

## Usage

```
$ docker run --rm ghcr.io/u6k/tagging-read-it-now pipenv run main
```

## Other

最新の情報は、[Wiki - bookmark - u6k.Redmine](https://redmine.u6k.me/projects/bookmark-bundler/wiki/Wiki)を参照してください。

### リリース手順

- リリース・ブランチを開始する
- TODOコメントを確認する
- バージョンを更新する
    - `.github/workflows/build-and-push.yml`
    - `tagging_read_it_now/__init__.py`
- CHANGELOGを最新化する
- CIの成功を確認する
- リリース・ブランチを終了する
- バージョンを更新して`-develop`サフィックスを追加する
- GitHubリリース・ノートを編集する

## Maintainer

- u6k
    - [Twitter](https://twitter.com/u6k_yu1)
    - [GitHub](https://github.com/u6k)
    - [Blog](https://blog.u6k.me/)

## Contributing

当プロジェクトに興味を持っていただき、ありがとうございます。[既存のチケット](https://redmine.u6k.me/projects/bookmark-bundler/issues/)をご覧ください。

当プロジェクトは、[Contributor Covenant](https://www.contributor-covenant.org/version/1/4/code-of-conduct)に準拠します。

## License

[MIT License](https://github.com/u6k/tagging-read-it-now/blob/main/LICENSE)
