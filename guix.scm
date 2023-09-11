;;;see example of using channels;https://ci.genenetwork.org/channels.scm
;; WIP(Js packaging)


(define-module (gn-markdown-editor)
  #:use-module (guix gexp)
  #:use-module (guix packages)
  #:use-module (guix download)
  #:use-module (guix git-download)
  #:use-module (guix build-system python)
  #:use-module (gnu packages)
  #:use-module (gnu packages python)
  #:use-module (gnu packages python-web)
  #:use-module (gnu packages python-xyz)
  #:use-module ((guix licenses) #:prefix license:))

;;redo

(package
  (name "gn-markdown-editor")
  (version "0.1")
  (source
    (origin
      (method git-fetch)
      (uri (git-reference
             (url "https://github.com/Alexanderlacuna/gn-markdown-editor.git")
             (commit (string-append "v" version))))
      (file-name (git-file-name name version))
      (sha256
       (base32
        "11hfx5x3jg4hyfxzav6ypsb57mahb5nk6qzg4zn1pyy1lilllqj6"))))
  (build-system python-build-system)
  (arguments `(#:tests? #f))
  (propagated-inputs (list python
         python-markdown
         python-pygithub
         python-flask ))
  (home-page "https://github.com/Alexanderlacuna/gn-markdown-editor")
  (synopsis "Gn-markdown-editor is a tiny web tool to preview Markdown formatted text.")
  (description "Gn-markdown-editor is a tiny web tool to preview Markdown formatted text.")
  (license license:gpl3))

