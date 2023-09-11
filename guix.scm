;;;see example of using channels;https://ci.genenetwork.org/channels.scm
;; WIP(Js packaging)


(use-modules
 (gnu packages python)
 (gnu packages python-web)
 (gnu packages python-xyz)
 (guix build-system python)
 (guix git-download)
 (guix download)
 (guix licenses)
 (guix packages))

(define-public gn-markdown
  (package
    (name "gn-markdown")
    (version "1.0")
    (source
      (origin
        (method url-fetch)
        (uri (pypi-uri "prov" version))
        (sha256
          (base32
            "1a9h406laclxalmdny37m0yyw7y17n359akclbahimdggq853jd0"))))
    (build-system python-build-system)
    (propagated-inputs
     `(("python" ,python)
       ("python-markdown" ,python-markdown)
       ("python-pygithub" , python-pygithub)
       ("python-flask" ,python-flask)))
    (home-page "https://github.com/Alexanderlacuna/gn-markdown-editor")
    (synopsis "Gn-markdown-editor is a tiny web tool to preview Markdown formatted text.")
    (description "Gn-markdown-editor is a tiny web tool to preview Markdown formatted text.")
    (license license:agpl3+)))

;;(define-public python-xyz gn-markdown)
