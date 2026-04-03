                                                                #HestaBit Learning & Development
                                                                            week 1


# Merge Postmortem

## Overview
This merge conflict occurred as part of a controlled experiment to understand how Git handles conflicting changes from multiple contributors working on the same repository.

Two separate clones of the same repository were created to simulate a real-world collaborative development scenario.

---

## Root Cause
Both clones independently modified the same line in `sample.txt`.Since these changes were made in parallel and committed separately, Git was unable to automatically determine which change should be kept when the branches were merged.As a result, Git flagged the file as conflicted during the pull
operation.

![](Images/clone.png)

![](Images/edit.png)

![](Images/pull.png)

---

## Resolution Process
The conflicted file was opened manually and the conflict markers inserted by Git were reviewed.

Instead of discarding one of the changes, both versions of the conflicting line were intentionally preserved by combining them
in the final file.

All conflict markers were removed, and the resolved file was staged and committed using a merge commit.

![](Images/pull_rebase.png)
---

## Outcome
The merge was completed successfully with no loss of information.Both contributors’ changes were retained, and the repository history now clearly reflects the merge through a dedicated merge commit.

## Graph
The following commit graph shows the branching and merging history,of the repository.

It clearly illustrates how two separate branches diverged after independent commits were made in different clones, followed by a merge commit that reconciled both histories into a single branch.

![](Images/graph.png)

