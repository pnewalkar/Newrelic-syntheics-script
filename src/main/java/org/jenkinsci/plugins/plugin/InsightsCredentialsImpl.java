package org.jenkinsci.plugins.plugin;

import com.cloudbees.plugins.credentials.CredentialsDescriptor;
import com.cloudbees.plugins.credentials.NameWith;
import com.cloudbees.plugins.credentials.impl.BaseStandardCredentials;
import edu.umd.cs.findbugs.annotations.CheckForNull;
import edu.umd.cs.findbugs.annotations.NonNull;
import hudson.Extension;
import hudson.util.Secret;
import org.kohsuke.stapler.DataBoundConstructor;

@NameWith(value = InsightsCredentialsNameProvider.class, priority = 50)
public class InsightsCredentialsImpl extends BaseStandardCredentials implements InsightsCredentials {
    @NonNull
    private final Secret apiKey;

    @NonNull
    private final String name;

    @NonNull
    private final String accountId;

    @DataBoundConstructor
    public InsightsCredentialsImpl(@CheckForNull String id,
                                @NonNull String name,
                                @CheckForNull String description,
                                @CheckForNull String apiKey,
                                @CheckForNull String accountId) {
        super(id, description);
        this.apiKey = Secret.fromString(apiKey);
        this.name = name;
        this.accountId = accountId;
    }

    @NonNull
    public Secret getApiKey() {
        return this.apiKey;
    }

    @NonNull
    public String getName() {
        return this.name;
    }

    @NonNull
    public String getAccountId() {
        return this.accountId;
    }

    @Extension
    public static class Descriptor
            extends CredentialsDescriptor {

        /** {@inheritDoc} */
        @Override
        public String getDisplayName() {
            return "New Relic Insights Key";
        }
    }
}

