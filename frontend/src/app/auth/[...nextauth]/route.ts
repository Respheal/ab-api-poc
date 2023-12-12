import NextAuth from "next-auth"

import CredentialsProvider from "next-auth/providers/credentials";
import GoogleProvider from "next-auth/providers/google";
import AppleProvider from "next-auth/providers/apple"
import DiscordProvider from "next-auth/providers/discord";
import LineProvider from "next-auth/providers/line";

import { User } from "@/client";

const handler = NextAuth({
  debug: (process.env.DEBUG =="true"),
  session: { strategy: "jwt" },
  providers: [
    CredentialsProvider({
      // The name to display on the sign in form (e.g. "Sign in with...")
      name: "Credentials",
      // `credentials` is used to generate a form on the sign in page.
      // You can specify which fields should be submitted, by adding keys to the `credentials` object.
      // e.g. domain, username, password, 2FA token, etc.
      // You can pass any HTML attribute to the <input> tag through the object.
      credentials: {
        username: { label: "Username", type: "text", placeholder: "jsmith" , "required": true},
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials, req) {
        // Add logic here to look up the user from the credentials supplied
        const user = { id: "1", name: "J Smith", email: "jsmith@example.com" }
  
        if (user) {
          // Any object returned will be saved in `user` property of the JWT
          return user
        } else {
          // If you return null then an error will be displayed advising the user to check their details.
          return null
  
          // You can also Reject this callback with an Error thus the user will be sent to the error page with the error message as a query parameter
        }
      }
    }),
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    }),
    AppleProvider({
      clientId: process.env.APPLE_ID,
      clientSecret: process.env.APPLE_SECRET
    }),
    DiscordProvider({
      clientId: process.env.DISCORD_CLIENT_ID,
      clientSecret: process.env.DISCORD_CLIENT_SECRET
    }),
    LineProvider({
      clientId: process.env.LINE_CLIENT_ID,
      clientSecret: process.env.LINE_CLIENT_SECRET
    })
  ],
  callbacks: {
    async jwt({ token, user, account, profile }) {
      if (account && profile) {
        // grab the user id from the DB, load that into the token
        // token.account = {provider: account.provider, id: account.providerAccountId}
        let abapiUser = await User.searchUser({oauth_id: account.providerAccountId, oauth_provider: account.provider})
        if (abapiUser) {token.uid = abapiUser.id}
        else {
          // The user doesn't exist; create them and load their id
          abapiUser = await User.createUser({email: profile.email, oauth_id: account.providerAccountId, oauth_provider: account.provider})
          token.uid = abapiUser.id
        }        
      }
      return token
    },
    async session({ session, user, token }) {
      return {...session, uid: token.uid}
    },
  }
})

export { handler as GET, handler as POST }