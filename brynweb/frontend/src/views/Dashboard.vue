<template>
  <div class="tile is-ancestor">
    <div class="tile is-vertical is-8">
      <div class="tile">
        <div class="tile is-parent is-vertical is-6">
          <article class="tile is-child notification is-primary">
            <p class="title has-text-centered">Servers</p>
            <nav class="level">
              <div class="level-item has-text-centered">
                <div>
                  <p class="heading">Servers</p>
                  <p class="title">3</p>
                </div>
              </div>
              <div class="level-item has-text-centered">
                <div>
                  <p class="heading">vCPUs</p>
                  <p class="title">12</p>
                </div>
              </div>
              <div class="level-item has-text-centered">
                <div>
                  <p class="heading">RAM / GB</p>
                  <p class="title">64</p>
                </div>
              </div>
            </nav>
          </article>
          <article class="tile is-child notification is-link">
            <p class="title has-text-centered">Volumes</p>
            <nav class="level">
              <div class="level-item has-text-centered">
                <div>
                  <p class="heading">Volumes</p>
                  <p class="title">2</p>
                </div>
              </div>
              <div class="level-item has-text-centered">
                <div>
                  <p class="heading">CAPACITY / GB</p>
                  <p class="title">500</p>
                </div>
              </div>
            </nav>
          </article>
        </div>
        <div class="tile is-parent is-vertical is-6">
          <article class="tile is-child notification is-link">
            <p class="title has-text-centered">Team Members</p>
            <nav class="level">
              <div class="level-item has-text-centered">
                <div>
                  <p class="heading">Users</p>
                  <p class="title">3</p>
                </div>
              </div>
              <div class="level-item has-text-centered">
                <div>
                  <p class="heading">Invitations</p>
                  <p class="title">2</p>
                </div>
              </div>
            </nav>
          </article>
          <article class="tile is-child notification is-primary">
            <p class="title has-text-centered">Licence</p>
            <p class="is-size-5 has-text-centered">
              <base-icon :icon="['fas', 'check']" class="mr-2" />
              Valid until 31/03/2021
            </p>
          </article>
        </div>
      </div>
      <div class="tile is-parent">
        <article class="tile is-child notification">
          <p class="title">Service status</p>
          <nav class="level is-mobile">
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Birmingham</p>
                <base-icon :icon="['fas', 'check']" size="large" />
              </div>
            </div>
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Warwick</p>
                <base-icon :icon="['fas', 'check']" size="large" />
              </div>
            </div>
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Cardif</p>
                <base-icon :icon="['fas', 'check']" size="large" />
              </div>
            </div>
            <div class="level-item has-text-centered">
              <div>
                <p class="heading">Swansea</p>
                <base-icon :icon="['fas', 'check']" size="large" />
              </div>
            </div>
          </nav>
        </article>
      </div>
    </div>
    <div class="tile is-parent">
      <article class="tile is-child notification is-success pr-2">
        <div style="max-height: 50vh; overflow-y: auto">
          <div class="content pr-5">
            <p class="title">Announcements</p>
            <p class="subtitle">
              £1.2 million from UKRI to support CLIMB infrastructure
            </p>
            <p>
              UKRI has announced today a cross-discipline investment for £213m
              to upgrade the UK’s world-class research infrastructure. The
              funding will help UK researchers tackle major challenges such as
              COVID-19 research and recovery and net-zero goals.
            </p>
            <a
              href="https://www.climb.ac.uk/1-2-million-from-ukri-to-support-climb-infrastructure/"
              >Read more...</a
            >
            <p>
              UKRI has announced today a cross-discipline investment for £213m
              to upgrade the UK’s world-class research infrastructure. The
              funding will help UK researchers tackle major challenges such as
              COVID-19 research and recovery and net-zero goals.
            </p>
            <a
              href="https://www.climb.ac.uk/1-2-million-from-ukri-to-support-climb-infrastructure/"
              >Read more...</a
            >
            <p>
              UKRI has announced today a cross-discipline investment for £213m
              to upgrade the UK’s world-class research infrastructure. The
              funding will help UK researchers tackle major challenges such as
              COVID-19 research and recovery and net-zero goals.
            </p>
            <a
              href="https://www.climb.ac.uk/1-2-million-from-ukri-to-support-climb-infrastructure/"
              >Read more...</a
            >
            <p>
              UKRI has announced today a cross-discipline investment for £213m
              to upgrade the UK’s world-class research infrastructure. The
              funding will help UK researchers tackle major challenges such as
              COVID-19 research and recovery and net-zero goals.
            </p>
            <a
              href="https://www.climb.ac.uk/1-2-million-from-ukri-to-support-climb-infrastructure/"
              >Read more...</a
            >
          </div>
        </div>
      </article>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  computed: mapState({
    hypervisorStats: (state) => state.hypervisorStats,
  }),
};
</script>