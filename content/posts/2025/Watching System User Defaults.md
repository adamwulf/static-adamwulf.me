+++
title = "Watching System User Defaults"
date = "2025-11-20T10:27:10+0000"
slug = "watching-system-user-defaults"
type = "post"
+++

Introducing **UserDefaultsWatcher**, the app where you can _watch user defaults_! Filter by Suite, Type, or filter query. Sort by any key, value, suite, type, or even last modified time. Available as a [free download](https://adamwulf.gumroad.com/l/user-defaults-watcher).

![UserDefaultsWatcher screenshot](/wp-content/uploads/2025/11/UserDefaultsWatcher.png)

I've recently implemented custom font sizes in [Muse](https://www.museapp.com), which has both an iPad and a Mac app. iOS provides access to the system's dynamic font size, but unfortunately on macOS the system setting is not available through any API.

I suspected that the macOS dynamic text size was stored in User Defaults in the system somewhere, but I had no idea how to track it down. At the time, I wanted an app that would show me all of the user defaults on the system - live updating - as well as let me sort by last modified. Then I could just have the app open to watch the defaults update as I changed the system's text size.

I did eventually find that macOS saves the system text size in `UIPreferredContentSizeCategoryName`, but unfortunately a sandbox'd Mac app isn't able to read it from the `NSGlobalDomain` defaults suite.

Still! Fun to find out, there's lots of gems in the user defaults, and having a way to spelunk through them felt clunky - until now!

[Download for free (or donation) on Gumroad](https://adamwulf.gumroad.com/l/user-defaults-watcher).