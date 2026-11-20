# Factory GitHub visibility

The factory wrapper owns labels, comments, pushes and PRs. Workers never write to GitHub directly. Labels: `factory` marks factory work, `factory:<worker>` or `factory:unowned` is the owner, and one stage label (`factory:building`, `factory:review`, `factory:changes-requested`, `factory:ready`) shows progress.
